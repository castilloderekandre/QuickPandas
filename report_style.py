from openpyxl import load_workbook
from pathlib import Path

class ReportStyle:
    @classmethod
    def style_sheet(cls, path: Path):
      wb = load_workbook(path)
      active_sheet = wb.active

      for column_cells in active_sheet.iter_cols():
        max_length = max(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
        active_sheet.column_dimensions[column_cells[0].column_letter].width = max_length + 2

      wb.save(path)