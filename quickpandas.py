import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import re
import math
import numpy as np
from pathlib import Path

schema = [ 'Mileage' ]
retail_inventory = pd.DataFrame(
        {
            'LAST 6 OF VIN': [], 
            'YEAR': [], 
            'MAKE': [], 
            'MODEL': [], 
            'MILEAGE': [], 
            'LOCATION': [], 
            'INVENTORY ($)': [], 
            'EXPENSES ($)': [], 
            'TOTAL INVESTED ($)': [], 
            'MISC.': [], 
            'SOURCED FROM': [], 
            'SRP ($)': [], 
            'DATE RECEIVED': [], 
            'OPEN INVOICE?': [], 
            'AGE': []
        })

def parse_description(description):
    schema_elements = []
    for identifier in schema:
        index = description.index(identifier) + len(identifier) + 1

        try:
            end_index = description.index('\n', index)
        except ValueError:
            end_index = len(description)
        
        schema_elements.append(description[index:end_index])

    return schema_elements

def parse_product_name(name):
    breakdown = []
    pattern = r":(\d+)\s+(\w+)\s+(.+)\(VIN#.+\)"
    capture_groups = re.search(pattern, name)
    if capture_groups:
        breakdown.extend(list(capture_groups.groups()))
    else:
        breakdown = ['-', '-', '-']
        
    return breakdown

def parse_product(index, product, expenses):
    vin = product.SKU[-6:]
    inventory = product['Purchase Cost']
    expenses = sum(expenses.loc[vin])
    product_series = [
        vin, # LAST 6 OF VIN
        *parse_product_name(product['Product/Service Name']), # YEAR, MAKE, MODEL
        *parse_description(product['Sales Description']), # MILEAGE (BASED ON SCHEMA)
        None, # LOCATION
        inventory, # INVENTORY
        expenses, # EXPENSES
        inventory + expenses, # TOTAL INVESTED
        None, # MISC
        None, # SOURCED FROM
        product['Sales Price / Rate'], # SRP
        None, # DATE RECEIVED
        None, # OPEN INVOICE
        f'=TODAY() - N{index+2}', # AGE
    ]

    return product_series

def create_retail_report(products, expenses):
    global retail_inventory
    for index, product in products.iterrows():
        parsed_product = parse_product(index, product, expenses)
        retail_inventory.loc[len(retail_inventory)] = parsed_product

def update_retail_inventory(old_retail_inventory):
    global retail_inventory
    retail_inventory['LOCATION'] = old_retail_inventory['LOCATION']
    retail_inventory['MISC.'] = old_retail_inventory['MISC.']
    retail_inventory['SOURCED FROM'] = old_retail_inventory['SOURCED FROM']
    retail_inventory['DATE RECEIVED'] = old_retail_inventory['DATE RECEIVED']
    retail_inventory['OPEN INVOICE?'] = old_retail_inventory['OPEN INVOICE?']


def on_import():
    global retail_inventory

    expenses = pd.read_excel('./Reports/Katy Truck and Equipment Sales LLC_CURRENT INVENTORY.xlsx')
    products_and_services = pd.read_excel('./Reports/ProductServiceList.xls')

    products = products_and_services.loc[products_and_services.Type == 'Inventory', ['Product/Service Name', 'Sales Description', 'SKU', 'Sales Price / Rate', 'Purchase Cost']]

    expenses = expenses.loc[[3, 9, 10, 11]]
    expenses = expenses.T
    expenses.columns = expenses.iloc[0]
    expenses = expenses[1:-1]
    expenses.set_index('Distribution account', inplace=True)

    def clean_index(index):
        return str(index).split('.')[0]

    expenses.index = expenses.index.map(clean_index)

    expenses.fillna(0, inplace=True)
    expenses = expenses.infer_objects(copy=False)

    create_retail_report(products, expenses)
    
    old_retail_inventory_path = Path('./Reports/retail_inventory.xlsx')

    if old_retail_inventory_path.exists():
        old_retail_inventory = pd.read_excel(old_retail_inventory_path)
        update_retail_inventory(old_retail_inventory)

    retail_inventory.to_excel('./Reports/retail_inventory.xlsx')

on_import()
