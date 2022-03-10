from bs4 import BeautifulSoup
import requests
import re, json
import time

url = 'http://duma.gov.ru/duma/deputies/7/'
headers = {
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/536.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
}

req = requests.get(url, headers=headers)
src = req.text

# with open('deputats.html', 'w') as file:
#     file.write()

# with open('deputats.html') as file:
#     src = file.read()

soup = BeautifulSoup(src, 'lxml')
bigSection = soup.find(class_='list-persons__wrapper')
sections= bigSection.find_all('section')
start = time.time()
links_list = []
main_info = []
iter = 1
for section in sections:
    items = section.find('ul', class_='list-persons').find_all(class_='list-persons__item')
    for item in items:
        link = 'http://duma.gov.ru' + item.find('a', class_='person__title__link').get('href')
        links_list.append(link)
    
for link in links_list:
    req = requests.get(link, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    person = soup.find(class_='person__container')
    s = soup.find(id='person-menu').find(class_='nav').find(class_='nav__list')
    try:
        name = person.find('img', class_='person__image').get('alt')
    except Exception as ex:
        print(ex)
        name = 'Имя не найдено'
    try:
        choosen_by = person.find(class_='article__lead').text.strip()
    except Exception as ex:
        print(ex)
        choosen_by = 'Нет избирательного участка'
    try:
        fraction = person.find(class_='person__description__link').text
    except Exception as ex:
        print(ex)
        fraction = 'Нет Фракции'
    try:
        description = person.find(class_='person__description__grid').find_all(class_='person__description__col')
        region = description[-1].text
    except Exception as ex:
        print(ex)
        region = 'Нет региона'
    try:
        salary_info_link = 'http://duma.gov.ru' + s.find('a', string=re.compile('Сведения о доходах')).get('href')
        req = requests.get(salary_info_link, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        current_year = 'http://duma.gov.ru' + soup.find('section').find('ul', class_='download__list').find('li', class_='download__item').find('a', class_='download__link').get('href')
    except Exception as ex:
        print(ex)
        salary_info_link = 'Кнопка не найдена'
    main_info.append({
            'Имя чиновника': name,
            'Ссылка на чиновника': link,
            'Кем выбран чиновник': choosen_by,
            'Партия чиновника': fraction,
            'Откуда чиновник': region,
            'Ссылка на файл с зп чиновника на текущий год': current_year,
})
    print(f'Депутат успешно записан. Выполнено {iter} из {len(links_list)}')
    iter+=1


with open('deputates_7.json', 'w', encoding='utf-8') as file:
    json.dump(main_info, file, indent=4, ensure_ascii=False)
    
end = time.time() - start
print(end)
    


    
