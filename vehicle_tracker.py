from pathlib import Path

class VehicleTracker:
  def __init__(self, vin) -> None:
    self.vin = vin
    self.list_of_paths: list[Path] = []
    self.list_of_values: list[dict] = []

  def add_path(self, path: Path):
    self.list_of_paths.append(path)

  def add_dict(self, dict: dict):
    self.list_of_values.append(dict)

  def add_data(self, path: Path, dict: dict):
    self.add_path(path)
    self.add_dict(dict)