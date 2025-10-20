import re

class DataTransform:
    inventory_fields = [
            'Product/Service Name', 
            'Sales Description', 
            'SKU',
            'Sales Price / Rate', 
            'Purchase Cost'
        ]

    def parse_description(description, schema):
        schema_elements = []
        for identifier in schema:
            description = str(description)
            index = description.find(identifier) 

            if (index == -1):
                schema_elements.append('Not Found')
                continue

            index += len(identifier) + 1

            end_index = description.find('\n', index)

            if (end_index == -1):
                end_index = len(description) - index + len(identifier)
            
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
        schema = [ 'Mileage' ]
        vin = product.SKU[-6:]
        in_inventory = product['Purchase Cost']
        expenses = sum(expenses.loc[vin])
        product_series = [
            vin, # LAST 6 OF VIN
            *DataTransform.parse_product_name(product['Product/Service Name']), # YEAR, MAKE, MODEL
            *DataTransform.parse_description(product['Sales Description'], schema), # MILEAGE (BASED ON SCHEMA)
            None, # LOCATION
            in_inventory, # in_inventory
            expenses, # EXPENSES
            in_inventory + expenses, # TOTAL INVESTED
            None, # MISC
            None, # SOURCED FROM
            product['Sales Price / Rate'], # SRP
            None, # DATE RECEIVED
            None, # OPEN INVOICE
            f'=TODAY() - N{index+2}', # AGE
        ]

        return product_series

    def clean_inventory(inventory):
        return inventory.loc[inventory.Type == 'Inventory', DataTransform.inventory_fields]

    def clean_expenses(expenses):
        expenses.to_excel('./Reports/expenses_dataframe.xlsx')

        expenses = expenses[3:]
        expenses = expenses.T
        expenses.iloc[0][3] = 'Class'
        expenses.columns = expenses.iloc[0]
        expenses = expenses[1:-1]
        expenses.set_index('Class', inplace=True)


        def clean_index(index):
            return str(index).split('.')[0]

        def clean_column(column):
            if column != str:
                column = str(column)
                return column.strip()

        expenses.index = expenses.index.map(clean_index)
        expenses.columns = expenses.columns.map(clean_column)

        expenses = expenses[['Detailing', 'Parts & Supplies', 'Transport Expense', 'Truck Fuel', 'Truck Repairs & Maintenance']]

        expenses.fillna(0, inplace=True)
        expenses = expenses.infer_objects(copy=False)

        return expenses
