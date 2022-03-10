import requests
from bs4 import BeautifulSoup
import json, csv
from time import sleep

url = 'http://www.lookatme.ru/flow/obschestvo/obschestvo/73111-50-samyih-rasprostranennyih-yazyikov-v-mire'
headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
}
req = requests.get(url, headers=headers)
src = req.text
# with open('languages.html', 'w') as file:
#     file.write(src)

# # Reading file
# with open('languages.html') as file:
#     src = file.read()

soup = BeautifulSoup(src, 'lxml')
table_heads = soup.find_all(class_='avant')
place = table_heads[0].text
language = table_heads[1].text
territory = table_heads[2].text
population = table_heads[3].text
with open('table.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            place,
            language,
            territory,
            population
        )
    )
table_data = soup.find(class_='border').find('tbody').find_all('tr')
table_info = []
iteration = 1
for item in table_data:
    table_tds = item.find_all('td')
    title = table_tds[0].text
    language = table_tds[1].text
    territory = table_tds[2].text
    population = table_tds[3].text

    table_info.append(

        {
            'Title': title,
            'Language': language,
            'Territory': territory,
            'Population': population
        }
    )

    with open('table.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                title,
                language,
                territory,
                population
            )
        )

    sleep(0.5)
    print(f'Сделано итераций: {iteration}, из 50. ')
    print('#' * 20)
    iteration += 1

with open('table.json', 'a', encoding='utf-8') as file:
    json.dump(table_info, file, indent=4, ensure_ascii=False)




# # Finding all divs with class CategoryTreeItem
# all_categories_hrefs = soup.find_all(class_='CategoryTreeItem')
# # iterate all elements in all_categories_hrefs
# all_categories_dict = {}
# for item in all_categories_hrefs:
#     # collecting all titles
#     item_text = item.text

#     # collecting all hrefs
#     item_href = 'https://ru.wikipedia.org' + item.find_next('a').get('href')

#     # adding text and hrefs in dict by key:value
#     all_categories_dict[item_text] = item_href

# # with open('all_categories.json', 'w') as file:
# #     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)
