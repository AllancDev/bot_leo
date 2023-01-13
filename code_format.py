# %%
import requests
from bs4 import BeautifulSoup as soup
import csv


a = requests.get('https://www.superoff.com.br/loja/catalogo.php')
a = soup(a.text)

element = a.find_all('li', {"class": "first-level sub"})

l = []
for el in element:
    l.append(el.a['href'])

sub = a.find('ul', {"class": 'sub-list second-level'}).ul
for i in sub:
    l.append(sub.li.a['href'])
# %%
for p in l:
    page = requests.get(l[0]).text
    products = soup(page)
    info = products.find_all('a', {"class": 'product-info'})
    products_name = []

    category_name = products.find('h1', {"class": "catalog-name"}).text
    
    for i in info:
        name = i.find('div', {'class': 'product-name'}).text
        price = i.find('span', {'class': 'current-price'}).text
        
        infos = {'product': name.strip(), 'price': price.strip(), 'category': category_name}
        products_name.append(infos)
        
    with open('./products.csv', "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        line = 0
        

        for p in products_name:
            if line == 0:
                writer.writerow(['product', 'price', 'category'])
            else: 
                writer.writerow([p['product'], p['price'], p['category']])
            line += 1
        file.close()

# %%
