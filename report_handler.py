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

    @classmethod
    def empty_inventory_schema(cls):
        empty_inventory = {field: [] for field in ReportHandler.retail_inventory_fields}
        return empty_inventory

    @classmethod
    def create_retail_inventory(cls, inventory: pd.DataFrame, expenses: pd.DataFrame):
        retail_inventory = pd.DataFrame(cls.empty_inventory_schema())

        for index, product in inventory.iterrows():
            retail_inventory.loc[len(retail_inventory)] = DataTransform.parse_product(index, product, expenses)

        return retail_inventory
         
    @classmethod
    def copy_manual_fields(cls, retail_inventory: pd.DataFrame, old_retail_inventory: pd.DataFrame):
      for vin in old_retail_inventory['LAST 6 OF VIN']:
        if vin in retail_inventory['LAST 6 OF VIN'].values:
          old_value = old_retail_inventory.loc[old_retail_inventory['LAST 6 OF VIN'] == vin].iloc[0]

          for field, manual_field in cls.retail_inventory_fields.items():
            if manual_field:
              retail_inventory.loc[
                 retail_inventory['LAST 6 OF VIN'] == vin, field
                ] = old_value[field]