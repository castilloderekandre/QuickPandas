import pandas as pd
from data_transform import DataTransform

class ReportHandler:
    retail_inventory_fields = {
            'LAST 6 OF VIN': False, 
            'YEAR': False, 
            'MAKE': False, 
            'MODEL': False, 
            'MILEAGE': False, 
            'LOCATION': False, 
            'INVENTORY ($)': False, 
            'EXPENSES ($)': False, 
            'TOTAL INVESTED ($)': False, 
            'MISC.': True, 
            'SOURCED FROM': True, 
            'SRP ($)': False, 
            'DATE RECEIVED': True, 
            'OPEN INVOICE?': True, 
            'AGE': False,
        }

    def empty_inventory_schema():
        empty_inventory = {field: [] for field in retail_inventory_fields}
        return empty_inventory

    def create_retail_report(inventory: pd.DataFrame, expenses: pd.DataFrame):
        retail_inventory = pd.DataFrame(empty_inventory_schema())

        for index, product in inventory.iterrows():
            parsed_product = DataTransform.parse_product(index, product, expenses)
            retail_inventory.loc[len(retail_inventory)] = parsed_product

        return retail_inventory

    def copy_manual_fields(old_retail_inventory: pd.DataFrame):
        for field, manual in self.retail_inventory_fields:
            if manual:
                self.retail_inventory[field] = old_retail_inventory[field]
