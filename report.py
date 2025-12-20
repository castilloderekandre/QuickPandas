import pandas as pd
from pathlib import Path
from data_processor import DataProcessor
from file_io import FileIO
from report_style import ReportStyle

class Report:
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

    def __init__(self, inventory_path: Path, expenses_path: Path, previous_retail_inventory_path: Path | None = None):
      self.inventory_path = inventory_path
      self.expenses_path = expenses_path
      self.previous_retail_inventory_path = previous_retail_inventory_path

    @classmethod
    def empty_inventory_schema(cls):
      empty_inventory = {field: [] for field in Report.retail_inventory_fields}
      return empty_inventory

    def load_files(self):
      self.inventory_df = DataProcessor.clean_inventory(FileIO.read_file(self.inventory_path))
      self.expenses_df = DataProcessor.clean_expenses(FileIO.read_file(self.expenses_path))
      
      if self.previous_retail_inventory_path:
        self.previous_retail_inventory = FileIO.read_file(self.previous_retail_inventory_path, True)

    def generate(self):
      self.load_files()
      
      self.retail_inventory = pd.DataFrame(Report.empty_inventory_schema())

      for index, product in self.inventory_df.iterrows():
        self.retail_inventory.loc[len(self.retail_inventory)] = DataProcessor.parse_product(index, product, self.expenses_df)

      if self.previous_retail_inventory_path:
        self.__class__.copy_manual_fields(self.retail_inventory, self.previous_retail_inventory)

      # new_index: list[int] = [num for num in range(1, len(self.retail_inventory) + 1)]
      # self.retail_inventory.index = new_index
      self.retail_inventory.index = pd.RangeIndex(1, len(self.retail_inventory) + 1)


    def to_file(self, output_path: Path):
      FileIO.write_file(self.retail_inventory, output_path)

    @classmethod
    def copy_manual_fields(cls, retail_inventory: pd.DataFrame, old_retail_inventory: pd.DataFrame):
      for vin in old_retail_inventory['LAST 6 OF VIN']:
        if vin in retail_inventory['LAST 6 OF VIN'].values:
          old_value = old_retail_inventory.loc[old_retail_inventory['LAST 6 OF VIN'] == vin].iloc[0]

          for field, manual_field in cls.retail_inventory_fields.items():
            if manual_field:
              if 'DATE RECEIVED' == field and old_value[field] is pd.Timestamp:
                old_value[field] = old_value[field].strftime('%m/%d/%Y')

              retail_inventory.loc[
                  retail_inventory['LAST 6 OF VIN'] == vin, field
                ] = old_value[field]
              
    def save(self, output_path: Path) -> None:
      self.to_file(output_path)
      ReportStyle.style_sheet(output_path)