from pathlib import Path
from tkinter import filedialog
import sys

class FileHandler:
    def __init__(self):
        self.paths = {}

    def select_file(self, key, label):
        path = filedialog.askopenfilename(
            title = 'Select Excel File',
            filetypes=[('Excel files', '*.xls'), ('Excel files', '*.xlsx')]
        )

        if not path:
            return
        
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).resolve().parent

        self.paths[key] = Path(path).absolute()
        label.configure(text=self.paths[key].name)

    def select_directory(self, key):
        path = filedialog.asksaveasfilename(
            title = 'Save As',
            defaultextension='.xlsx',
            filetypes=[('Excel files', '*.xlsx')]
        )

        if not path:
            return

        self.paths[key] = Path(path).absolute()
