import re
import json
import requests
import datetime
from bs4 import BeautifulSoup

url_base = 'https://www.cyberpuerta.mx/Computadoras/Laptops/'
date = datetime.datetime.now().date()
full_info = []

def get_paginas():
    try:
        return int(input('Numero de paginas: '))
    except:
        print('Dar un numero valido')
        return get_paginas()

def scrape_page(page_number, paginas):
    response = requests.get(url_base+page_number)
    print(f'Escrapeando pagina {page_number} de {paginas}\tStatus: {response.status_code}', end = '\r')
    
    soup = BeautifulSoup(response.content, 'lxml')
    derechas = soup.select('div.emproduct>form>div.emproduct_right')
    nombres = [x.a.text.strip('\n') for x in derechas]
    skus = [x.select('div.emproduct_right_artnum')[0].text.strip('\n') for x in derechas]
    infos = [x.select('div.emproduct_left_attribute_price')[0] for x in derechas]
    specs = [[y.text for y in x.select('div.emproduct_right_attribute>ul>li')] for x in infos]
    precios = [x.select('div.emproduct_right_price')[0].select('label.price')[0].text.strip('\n')
           for x in derechas]
    
    for na, sk, sp, pr in zip(nombres, skus, specs, precios):
        all_specs = [f'Nombre: {na}']+[sk]+sp+[f'Precio: {pr}']+[f'Date: {date}']
        full_info.append({key.strip(',\n '): ':'.join(val).strip(',\n ') for key,*val in 
                          [pair.split(':') for pair in all_specs]})
        
def main(paginas):
    
    for i in range(1,paginas+1):
        scrape_page(str(i), paginas)
        
    with open(f'productos_cyberpuerta_{date}.json', 'w') as f:
        json.dump(full_info, f)
    print('Proceso terminado'+' '*100)
    
if __name__ == '__main__':
    
    main(get_paginas())