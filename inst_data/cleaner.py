with open('data.txt', 'r') as file:
    file_urls = file.readlines()

new_urls = []
for url in file_urls:
    if url not in new_urls:
        new_urls.append(url)

with open('cleaned_data.txt', 'a') as file:
    for i in new_urls:
        file.write(i)