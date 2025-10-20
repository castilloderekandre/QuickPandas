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
        empty_inventory = {field: [] for field in ReportHandler.retail_inventory_fields}
        return empty_inventory

    def create_retail_inventory(inventory: pd.DataFrame, expenses: pd.DataFrame):
        retail_inventory = pd.DataFrame(ReportHandler.empty_inventory_schema())

        for index, product in inventory.iterrows():
            retail_inventory.loc[len(retail_inventory)] = DataTransform.parse_product(index, product, expenses)

        return retail_inventory

    def copy_manual_fields(retail_inventory, old_retail_inventory: pd.DataFrame):
        for field, manual in ReportHandler.retail_inventory_fields:
            if manual:
                retail_inventory[field] = old_retail_inventory[field]
