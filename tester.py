from pathlib import Path
from report import Report

def generate_reports(inventory_list: list[Path], expenses_list: list[Path]) -> None:
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
    report.save(Path(f'./retail_inventory_phase_{count}'))
    count += 1

def count_if(predicate):
  pass