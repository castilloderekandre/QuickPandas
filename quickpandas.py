import pandas as pd
import re
import math

schema = [ 'Mileage' ]
retail_report = pd.DataFrame(
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

def parse_expense(vin, source_expenses_report):
    expenses_report = source_expenses_report.fillna(0)
    distribution_account = expenses_report.iloc[3]
    expense_list = [0, 0, 0]
    expenses = 0
    for i in range(len(distribution_account)):
        account = distribution_account.iloc[i]
        if isinstance(account, (int, float)):
            account = math.trunc(account)
            account = str(account)

        if not vin in account:
            continue

        expenses += expenses_report.iloc[9].iloc[i]
        expenses += expenses_report.iloc[10].iloc[i]
        expenses += expenses_report.iloc[11].iloc[i]
        
        expense_list[0] = expenses_report.iloc[12].iloc[i]
        expense_list[1] = expenses
        expense_list[2] = expense_list[0] + expense_list[1]

    return expense_list


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
    pattern = r"Truck:(\d+)\s+(\w+)\s+((?:\w+\s)+)\(VIN#.+\)"
    capture_groups = re.search(pattern, name)
    if capture_groups:
        breakdown.extend(list(capture_groups.groups()))
    else:
        breakdown = ['', '', '']
        
    return breakdown

def parse_product(index, product, expenses):
    product_series = [
        product.SKU[-6:], 
        *parse_product_name(product['Product/Service Name']), 
        *parse_description(product['Sales Description']),
        None,
        *parse_expense(product.SKU[-6:], expenses),
        None,
        None,
        product['Sales Price / Rate'],
        None,
        None,
        f'=TODAY() - N{index+2}',
    ]

    parse_expense(product_series[0], expenses)

    return product_series

def create_retail_report(products, expenses):
    global retail_report
    for index, product in products.iterrows():
        parsed_product = parse_product(index, product, expenses)
        retail_report.loc[len(retail_report)] = parsed_product



def on_import():
    expenses = pd.read_excel('./Reports/Katy Truck and Equipment Sales LLC_CURRENT INVENTORY.xlsx')
    products_and_services = pd.read_excel('./Reports/ProductServiceList.xls')

    # print(expenses)

    products = products_and_services.loc[products_and_services.Type == 'Inventory', ['Product/Service Name', 'Sales Description', 'SKU', 'Sales Price / Rate', 'Purchase Cost']]
    create_retail_report(products, expenses)
    retail_report.to_excel('./Reports/retail_report.xlsx')

on_import()
