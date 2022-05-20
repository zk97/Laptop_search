import re
import json
import requests
import datetime
from bs4 import BeautifulSoup

url_base = 'https://intercompras.com/c/laptops-686?page='
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
    derecha = soup.select('div.divProductListInfoProductFlex')
    nombres = [x.select('div.divProductListTitle')[0].text.strip('\n ') for x in derecha]
    modelos = [x.select('div.divProductListFeature.model')[0].text.strip('\n ') for x in derecha]
    specs = [[y.text.strip('\n ')
              for y in x.select('div.divProductListFeaturesContainer')[0].select('div.divProductListFeature')]
             for x in derecha]
    precios = [x.select('div.divProductListPriceContainer > div.divProductListPrice')[0].text.strip('\n ')
               for x in derecha]
    
    for na, mod, sp, pr in zip(nombres, modelos, specs, precios):
        all_specs = [f'Nombre: {na}']+[mod]+sp+[f'Precio: {pr}']+[f'Date: {date}']
        full_info.append({key.strip('\n, '): ':'.join(val).strip('\n, ') for key,*val in 
                          [pair.split(':') for pair in all_specs]})
        
def main(paginas):
    
    for i in range(1,paginas+1):
        scrape_page(str(i), paginas)
        
    with open(f'productos_intercompras_{date}.json', 'w') as f:
        json.dump(full_info, f)
    print('Proceso terminado'+' '*100)
    
if __name__ == '__main__':
    
    main(get_paginas())