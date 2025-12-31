from pathlib import Path
from Report_Builder.report import Report
from typing import Callable, Dict
import pandas as pd
from vehicle_tracker import VehicleTracker
import pprint

class DiagnosticCompiler:

  def __init__(self) -> None:
    self.BASE_FILE_NAME = 'retail_inventory_phase_'
    self.list_df: list[pd.DataFrame] = []
    self.REPORT_PATH = Path('C:\\Taji\\GitHub\\QuickPandas\\Reports\\')
    self.report_list: list[Report] = []
    self.vehicle_fields_dict: dict[str, VehicleTracker] = {}

  def autorun(self) -> None:
    inventory_paths: list[Path] = self.get_paths_from(self.REPORT_PATH, 'inventory_*.xls')
    expense_paths: list[Path] = self.get_paths_from(self.REPORT_PATH, 'expenses_*.xlsx')

    self.generate_reports(inventory_paths, expense_paths)

    self.make_vehicle_trackers()
    
    for vehicle_tracker in self.vehicle_fields_dict.values():
      vehicle_tracker.get_history()

    # pprint.pprint(list(self.vehicle_fields_dict.values())[0].vin)
    # pprint.pprint(list(self.vehicle_fields_dict.values())[0].history)
    # self.use_named_tuples()
    

  def make_vehicle_trackers(self) -> None:
    for report in self.report_list:
      for _, row in report.retail_inventory.iterrows():

        vin = row['LAST 6 OF VIN']
        if vin not in self.vehicle_fields_dict:
          self.vehicle_fields_dict[vin] = VehicleTracker(vin)

        self.vehicle_fields_dict[vin].add_data(report.export_path, row)
    
  def use_named_tuples(self) -> None: 
    for report in self.report_list:
      df = report.retail_inventory
      for row in df.itertuples():
        vin_: str = str(row._1)
        if vin_.__eq__('KP2197'):
          print(row)


  def get_paths_from(self, path: Path, file_globbing_expression: str) -> list[Path]:
    """
    Returns a list of `Path` for each file matching the `file_globbing_expression`
    
    :param self: Description
    :param path: Initial path
    :type path: Path
    :param file_globbing_expression: File glob expression
    :type file_globbing_expression: str
    :return: List of `Path` for each file matching the `file_globbing_expression`
    :rtype: list[Path]
    """
    path_list: list[Path] = list(path.glob(file_globbing_expression))
    return path_list

  def generate_reports(self, inventory_list: list[Path], expenses_list: list[Path]) -> None:
    """
    Generates reports from two ordered lists (of equal length) of paths (inventory and expenses files)
    
    :param self: Description
    :param inventory_list: List of inventory Excel file's paths
    :type inventory_list: list[Path]
    :param expenses_list: List of expense Excel file's paths
    :type expenses_list: list[Path]
    """

    count: int = 1
    for inventory_path, expenses_path in zip(inventory_list, expenses_list):
      if count == 1:
        count += 1
        continue

      report: Report = Report(inventory_path, expenses_path)
      if count > 1:
        report: Report = Report(inventory_path, expenses_path, Path(f'{self.REPORT_PATH}\\{self.BASE_FILE_NAME}{count-1}.xlsx'))
      else:
        report: Report = Report(inventory_path, expenses_path, Path("C:\\Taji\\GitHub\\QuickPandas\\Reports\\edited_retail_inventory.xlsx"))
      

      report.generate()
      self.report_list.append(report)

      self.list_df.append(report.retail_inventory)
    
      report.save(Path(f'{self.REPORT_PATH}\\{self.BASE_FILE_NAME}{count}.xlsx'))
      
      count += 1

  def save_reports(self):
    # for report in self.list_df:
    pass

  def rows_where(self, list_df: list[pd.DataFrame], predicate_func: Callable[[pd.Series], bool]) -> list[pd.Series]:
    """ Returns a list of `pandas.Series` objects where `predicate_func` returned `True`
    
    :param self: Description
    :param list_df: List of `pandas.DataFrame` generated from `Report` class
    :type list_df: list[pd.DataFrame]
    :param predicate_func: Predicate that returns a `bool`
    :type predicate_func: Callable[[pd.Series], bool]
    :return: List of `pandas.Series` where `predicate_func` return `True`
    :rtype: list[Series[Any]]
    """
    list_true: list[pd.Series] = []
    for df in list_df:
      for _, row in df.iterrows():
        if predicate_func(row):
          list_true.append(row)

    return list_true

diagnostic = DiagnosticCompiler()
diagnostic.autorun()