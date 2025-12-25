from pathlib import Path
from report_builder.report import Report
import pandas as pd

class Tester:
  def __init__(self) -> None:
    self.list_df: list[pd.DataFrame] = []
    pass

  def generate_reports(self, inventory_list: list[Path], expenses_list: list[Path]) -> None:
    """
      Generates reports from two ordered lists (of equal length) of paths (inventory and expenses)

      Args:
          inventory_list (list[pd.DataFrame]): List of inventory paths.
          expenses_list (list[pd.DataFrame]): List of expenses paths.

      Returns: None
    """
    count = 1
    for inventory_path, expenses_path in zip(inventory_list, expenses_list):

      report = Report(inventory_path, expenses_path)
      if count > 1:
        report = Report(inventory_path, expenses_path, Path(f'./retail_inventory_phase_{count-1}'))
      
      report.generate()

      self.list_df.append(report.retail_inventory)
      
      report.save(Path(f'./retail_inventory_phase_{count}'))
      count += 1

  def count_if(self, predicate) -> int:
    for retail_inventory_df in self.list_df:
      retail_inventory_df.
    return -1