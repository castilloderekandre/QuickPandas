from pathlib import Path
from report_builder.report import Report
from typing import Callable
import pandas as pd

class Tester:
  def __init__(self) -> None:
    self.base_file_name = 'retail_inventory_phase_'
    self.list_df: list[pd.DataFrame] = []

  def get_paths_from(self, path: Path, file_globbing_expression: str) -> list[Path]:
    path_list: list[Path] = list(path.glob(file_globbing_expression))
    return path_list

  def generate_reports(self, inventory_list: list[Path], expenses_list: list[Path]) -> None:
    """
      Generates reports from two ordered lists (of equal length) of paths (inventory and expenses files)

      Args:
          inventory_list (list[pd.DataFrame]): List of inventory paths.
          expenses_list (list[pd.DataFrame]): List of expenses paths.

      Returns: None
    """
    count: int = 1
    for inventory_path, expenses_path in zip(inventory_list, expenses_list):

      report: Report = Report(inventory_path, expenses_path)
      if count > 1:
        report: Report = Report(inventory_path, expenses_path, Path(f'./retail_inventory_phase_{count-1}.xlsx'))
      
      report.generate()

      self.list_df.append(report.retail_inventory)
      
      report.save(Path(f'./{self.base_file_name}{count}'))
      count += 1

  def track_row_where(self, list_df: list[pd.DataFrame], predicate: Callable[[pd.Series], bool]) -> list[pd.Series]:
    list_true: list[pd.Series] = []
    for df in list_df:
      for _, row in df.iterrows():
        if predicate(row):
          list_true.append(row)

    return list_true