from calendar import c
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os

""" Автор скрипта PythonToday, но были внесены дополнения связанные с расширением функционала """

class InstagramBot():


    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("/Users/nikita/Documents/pyfiles/chromedriver")

    # метод для закрытия браузера
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    # метод логина
    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(self.username)

        time.sleep(2)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(self.password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    # метод ставит лайки по hashtag
    def like_photo_by_hashtag(self, hashtag):

        browser = self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(5)

        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        hrefs = browser.find_elements_by_tag_name('a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(80, 100))
            except Exception as ex:
                print(ex)
                self.close_browser()

    # метод проверяет по xpath существует ли элемент на странице
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # метод ставит лайк на пост по прямой ссылке
    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(2)

            like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(2)

            print(f"Лайк на пост: {userpost} поставлен!")
            self.close_browser()

    # метод собирает ссылки на все посты пользователя
    def get_all_posts_urls(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(2)

            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    # метод ставит лайки по ссылке на аккаунт пользователя
    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list[0:6]:
                try:
                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    # time.sleep(random.randrange(80, 100))
                    time.sleep(2)

                    print(f"Лайк на пост: {post_url} успешно поставлен!")
                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    # метод скачивает контент со страницы пользователя
    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")
        else:
            os.mkdir(file_name)

        img_and_video_src_urls = []
        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(4)

                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # сохраняем изображение
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # сохраняем видео
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                    else:
                        # print("Упс! Что-то пошло не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки!")
                    print(f"Контент из поста {post_url} успешно скачан!")

                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")

    # метод подписки на всех подписчиков переданного аккаунта
    def get_all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # создаём папку с именем пользователя для чистоты проекта
        if os.path.exists(f"inst_data/{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(f'inst_data/{file_name}')

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(2)

            followers_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
            followers_count = browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span').text
            followers_count = int(''.join(followers_count.split(' ')))
            print(f"Количество подписчиков: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 8)
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)
            try:
                followers_ul = browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[2]/ul")
            except Exception as ex:
                print('Защита сработала)')
                followers_ul = browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[2]/ul")

            time.sleep(4)
            
            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script(f"return document.querySelector('.jSC57').scrollIntoView(0, 648);")
                    time.sleep(random.randrange(2,4))
                    all_urls_div = followers_ul.find_elements_by_tag_name('li')
                    print(len(all_urls_div))
                    if len(all_urls_div) == followers_count:
                        break
                    print(f"Итерация #{i}")

                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # сохраняем всех подписчиков пользователя в файл
                with open(f"inst_data/{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

            except Exception as ex:
                print(ex)
                input('Подтвердите выход => ')
                self.close_browser()
        input('Подтвердите выход => ')
        self.close_browser()

    # метод для отправки сообщений в директ
    def send_direct_message(self, usernames="", message="", img_path=''):

        browser = self.browser
        time.sleep(random.randrange(2, 4))

        direct_message_button = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"

        if not self.xpath_exists(direct_message_button):
            print("Кнопка отправки сообщений не найдена!")
            self.close_browser()
        else:
            print("Отправляем сообщение...")
            direct_message = browser.find_element_by_xpath(direct_message_button).click()
            time.sleep(random.randrange(2, 4))

        # отключаем всплывающее окно
        if self.xpath_exists("/html/body/div[6]/div/div"):
            browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[2]").click()
        time.sleep(random.randrange(2, 4))

        send_message_button = browser.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/div[3]/div/button").click()
        time.sleep(random.randrange(2, 4))
        counter = 0
        # отправка сообщения пользователям
        for user in usernames:
            # вводим получателя
            to_input = browser.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div[1]/div/div[2]/input")
            to_input.send_keys(user)
            time.sleep(random.randrange(5, 7))

            # выбираем получателя из списка
            users_list = browser.find_element_by_xpath(
                "/html/body/div[6]/div/div/div[2]/div[2]/div[1]/div").find_element_by_tag_name("button").click()
            time.sleep(random.randrange(5, 7))

            next_button = browser.find_element_by_xpath(
                "/html/body/div[6]/div/div/div[1]/div/div[2]/div/button").click()
            time.sleep(random.randrange(5, 7))
            try:
                if message:
                    text_message_area = browser.find_element_by_xpath(
                    "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
                text_message_area.clear()
                text_message_area.send_keys(message)
                time.sleep(5)
                send_button = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button').click()
                counter += 1
                print(f"Сообщение для {user} успешно отправлено! Отправлено сообщений: {counter} из {len(usernames)}")
                time.sleep(random.randrange(5, 7))
            except Exception as ex:
                print(f'Ошибка - {ex}')
                input('Подтвердите продолжение ==> ')

            find_new_message_button = browser.find_element_by_xpath('/html/body/div[1]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button').click()

        # отправка изображения
            if img_path:
                send_img_input = browser.find_element_by_xpath("/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
                send_img_input.send_keys(img_path)
                print(f"Изображение для {usernames} успешно отправлено!")
                time.sleep(random.randrange(2, 4))

        self.close_browser()

    def urls_to_usernames(self, file_name):
        with open(f'inst_data/{file_name}.txt', 'r') as file:
            urls = file.readlines()
            usernames = []
            for row in urls:
                if row not in usernames:
                    no_space = row.split('\n')
                    elem = no_space[0].split('/')
                    username = elem[-2]
                    if username in ('users', 'to', 'skip'):
                        continue
                    usernames.append(username)
        print(f'Список пользователей сформирован успешно. Сообщения будут отправлены {len(usernames)} пользователям из {len(urls)}')
        return usernames


username = int(input('Введите username пользователя: '))
bot = InstagramBot('your_username', 'your_password')
bot.login()
# urodec.get_all_followers(f'https://www.instagram.com/{username}/')
bot.send_direct_message(bot.urls_to_usernames(file_name='your_file_name'), "your message", "your image")
