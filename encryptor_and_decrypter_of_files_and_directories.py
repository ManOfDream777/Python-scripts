import base64
import os

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class AESFileEncryptor:
    def __init__(self, key):
        self.key = key

    def encrypt_data(self, data):
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        encrypted = iv + cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt_data(self, encrypted_data):
        encrypted_data = base64.urlsafe_b64decode(encrypted_data.encode())
        iv = encrypted_data[:16]
        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        decrypted = cipher.decrypt(encrypted_data[16:]).decode()
        return decrypted

    def encrypt_file(self, file_path):
        iv = get_random_bytes(16)
        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)

        with open(file_path, 'rb') as f:
            plaintext = f.read()

        ciphertext = cipher.encrypt(plaintext)

        with open(file_path + '.enc', 'wb') as f:
            f.write(iv + ciphertext)

        os.remove(file_path)

    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as f:
            iv = f.read(16)
            ciphertext = f.read()

        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        plaintext = cipher.decrypt(ciphertext)

        with open(file_path[:-4], 'wb') as f:
            f.write(plaintext)

        os.remove(file_path)


class DirectoryEncryptor:
    def __init__(self, key: bytes):
        self.encryptor = AESFileEncryptor(key)

    def process_directory(self, path, encrypt=True):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if encrypt and not file.endswith('.enc'):
                    self.encryptor.encrypt_file(file_path)
                elif not encrypt and file.endswith('.enc'):
                    self.encryptor.decrypt_file(file_path)

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                parent_path = os.path.dirname(dir_path)
                if encrypt:
                    encrypted_dir_name = self.encryptor.encrypt_data(dir)
                else:
                    encrypted_dir_name = self.encryptor.decrypt_data(dir)

                new_dir_path = os.path.join(parent_path, encrypted_dir_name)
                os.rename(dir_path, new_dir_path)

    def encrypt_directories(self, base_path):
        items = os.listdir(base_path)
        for item in items:
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                self.process_directory(item_path, encrypt=True)

                encrypted_dir_name = self.encryptor.encrypt_data(os.path.basename(item_path))
                new_dir_path = os.path.join(base_path, encrypted_dir_name)
                os.rename(item_path, new_dir_path)

    def decrypt_directories(self, base_path):
        items = os.listdir(base_path)
        for item in items:
            item_path = os.path.join(base_path, item)
            if os.path.isdir(item_path):
                self.process_directory(item_path, encrypt=False)

                decrypted_dir_name = self.encryptor.decrypt_data(os.path.basename(item_path))
                new_dir_path = os.path.join(base_path, decrypted_dir_name)
                os.rename(item_path, new_dir_path)


if __name__ == '__main__':
    """ Применение """
    key = get_random_bytes(32)
    encryptor = DirectoryEncryptor(key)

    base_directory = os.path.dirname(os.path.abspath(__file__))

    encryptor.encrypt_directories(base_directory)

    encryptor.decrypt_directories(base_directory)
