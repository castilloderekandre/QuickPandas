from tkinter import filedialog

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

        self.paths[key] = Path(path)
        label.configure(text=self.paths[key].name)

    def select_directory(self, key):
        path = filedialog.asksaveasfile(
            title = 'Save As',
            filetypes=[('Excel files', '*.xlsx')]
        )

        if not path:
            return

        self.paths[key] = path
