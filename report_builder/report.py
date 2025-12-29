import pandas as pd
from pathlib import Path
from Report_Builder import DataProcessor
from Report_Builder.file_io import FileIO
from Report_Builder.report_style import ReportStyle

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
      self.inventory_path: Path = inventory_path
      self.expenses_path: Path = expenses_path
      self.previous_retail_inventory_path: Path | None = previous_retail_inventory_path
      self.export_path: Path = Path()

    @classmethod
    def empty_inventory_schema(cls) -> dict[str, list]:
      empty_inventory: dict = {field: [] for field in Report.retail_inventory_fields}
      return empty_inventory

    def load_files(self):
      self.inventory_df: pd.DataFrame = DataProcessor.clean_inventory(FileIO.read_file(self.inventory_path))
      self.expenses_df: pd.DataFrame = DataProcessor.clean_expenses(FileIO.read_file(self.expenses_path))
      
      if self.previous_retail_inventory_path:
        self.previous_retail_inventory = FileIO.read_file(self.previous_retail_inventory_path, True)

    def generate(self):
      self.load_files()
      
      self.retail_inventory = pd.DataFrame(Report.empty_inventory_schema())

      for index, product in self.inventory_df.iterrows():
        self.retail_inventory.loc[len(self.retail_inventory)] = DataProcessor.parse_product(index, product, self.expenses_df)

      if self.previous_retail_inventory_path:
        self.__class__.copy_manual_fields_in_place(self.previous_retail_inventory, self.retail_inventory)

      # new_index: list[int] = [num for num in range(1, len(self.retail_inventory) + 1)]
      # self.retail_inventory.index = new_index
      self.retail_inventory.index = pd.RangeIndex(1, len(self.retail_inventory) + 1)


    def to_file(self, output_path: Path):
      FileIO.write_file(self.retail_inventory, output_path)

    @classmethod
    def copy_manual_fields_in_place(cls, from_retail_inventory: pd.DataFrame, to_retail_inventory: pd.DataFrame):
      manual_fields: list[str] = [field for field in cls.retail_inventory_fields.keys() if field]
      
      # manual_fields_df = from_retail_inventory[['LAST 6 OF VIN', *manual_fields]]

      to_vin_list: pd.Series = to_retail_inventory['LAST 6 OF VIN']
      from_vin_list: pd.Series = from_retail_inventory['LAST 6 OF VIN']

      def find(value: str, series: pd.Series) -> int:
        for i, v in enumerate(series):
          if v == value:
            return i
          
        return -1

      for to_vin in to_vin_list.values:

        from_row_position = find(to_vin, from_vin_list)
        if from_row_position == -1:
          continue

        to_row_position = find(to_vin, to_vin_list)

        for field in manual_fields:
            # if 'DATE RECEIVED' == field and previous_value[field] is pd.Timestamp:
              # previous_value[field] = previous_value[field].strftime('%m/%d/%Y') # FORMATTING TIMESTAMP

            to_retail_inventory.loc[to_row_position, field] = from_retail_inventory.loc[from_row_position, field]
        
    def save(self, export_path: Path) -> None:
      self.to_file(export_path)
      self.export_path = export_path
      ReportStyle.style_sheet(export_path)