import json
import configparser
from pymongo import MongoClient

def get_table_name():
    
    tablas = {'1':'cyberpuerta'}
    table_number = input("Seleccionar página (insertar número corresponiente):\n1) Cyberpuerta\n")
    if not table_number in tablas:
        print('Favor de seleccionar un numero válido, opciones: [1]')
        return get_table_name()
    return tablas[table_number]

def get_mongo_config():
    config = configparser.ConfigParser()
    config.read('config.conf')
    return config['MONGO']

def conect_table(config, table_name):
    path_mongo = f'mongodb+srv://{config["user"]}:{config["password"]}{config["cluster"]}'
    client = MongoClient(path_mongo)
    laptops = client['laptops']
    return laptops[table_name]

def update_table(table, page):
    table.delete_many({})
    
    with open(f'productos_{page}.json') as f:
        productos = json.load(f)
    table.insert_many(productos)
        
def main():
    page_name = get_table_name()
    config = get_mongo_config()
    table = conect_table(config, page_name)
    update_table(table, page_name)
    print('Proceso terminado')
    
if __name__ == '__main__':
    main()