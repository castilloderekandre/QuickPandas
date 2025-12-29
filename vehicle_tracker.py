from pathlib import Path
from Report_Builder.report import Report
import pandas as pd

class VehicleTracker:

  def __init__(self, vin) -> None:
    self.vin = vin
    self.list_of_inventory_paths: list[Path] = []
    self.list_of_expense_paths: list[Path] = []
    self.list_of_paths: list[Path] = []
    self.list_of_data: list[pd.Series] = []
    self.history: dict[str, list] = {}
    self.indexes = Report.retail_inventory_fields.keys()

  def add_path(self, path: Path) -> None:
    self.list_of_paths.append(path)

  def add_series(self, series: pd.Series) -> None:
    self.list_of_data.append(series)

  def add_data(self, path: Path, series: pd.Series) -> None:
    self.add_path(path)
    self.add_series(series)

  def get_history(self) -> None:
    self.history = self.diff_data()

  def diff_data(self) -> dict[str, list]:
    """
    Docstring for diff_data
    
    :param self: Description
    :return: Description
    :rtype: dict[str, list[Any]]
    """

    diff: dict[str, list] = {}
    for index in self.indexes:
      diff[index] = []
      value = None
      for series in self.list_of_data:

        if value != series[index]:
          diff[index].append(series[index])

        value = series[index]  

    return diff
