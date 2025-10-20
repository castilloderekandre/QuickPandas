import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import math
import numpy as np
import customtkinter as ctk

from file_handler import FileHandler
from file_io import FileIO
from data_transform import DataTransform
from report_handler import ReportHandler

from pathlib import Path
from CTkMessagebox import CTkMessagebox


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.app_title = 'Reportwise'
        self.title(self.app_title)

        self.count = 0

        self.PRODUCTS_KEY = 'products'
        self.EXPENSES_KEY = 'expenses'
        self.INVENTORY_KEY = 'inventory'
        self.OUTPUT_KEY = 'output'

        self.filehandler = FileHandler()

        self.label_1 = ctk.CTkLabel(self, text='Products/Services Excel File')
        self.label_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky='ew')

        self.label_2 = ctk.CTkLabel(self, text='Expenses Excel File')
        self.label_2.grid(row=0, column=1, padx=10, pady=(10, 0), sticky='ew')

        self.label_3 = ctk.CTkLabel(self, text='Previous Retail Inventory Excel File')
        self.label_3.grid(row=0, column=2, padx=10, pady=(10, 0), sticky='ew')

        #
        self.button_select_products_file = ctk.CTkButton(self, text='Select File', command=lambda: self.filehandler.select_file(self.PRODUCTS_KEY, self.label_products_basename))
        self.button_select_products_file.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        
        self.label_products_basename = ctk.CTkLabel(self, text='No File Selected')
        self.label_products_basename.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        #
        self.button_select_expenses_file = ctk.CTkButton(self, text='Select File', command=lambda: self.filehandler.select_file(self.EXPENSES_KEY, self.label_expenses_basename))
        self.button_select_expenses_file.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        self.label_expenses_basename = ctk.CTkLabel(self, text='No File Selected')
        self.label_expenses_basename.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        #
        self.button_select_inventory_file = ctk.CTkButton(self, text='Select File', command=lambda: self.filehandler.select_file(self.INVENTORY_KEY, self.label_inventory_basename))
        self.button_select_inventory_file.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

        self.label_inventory_basename = ctk.CTkLabel(self, text='No File Selected')
        self.label_inventory_basename.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

        #
        self.button_save_as = ctk.CTkButton(self, text='Save As', command=self.save_as)
        self.button_save_as.grid(row=3, column=0, padx=10, pady=10, columnspan=3, sticky='ew')

        #
        self.schema = [ 'Mileage' ]

        self.update_idletasks()

    def show_popup(self, report):
        CTkMessagebox(title="Info", message="A file has not been selected. Cannot create report!") 

    def save_as(self):
        if not self.PRODUCTS_KEY in self.filehandler.paths:
            self.show_popup('Products/Services')
            return

        if not self.EXPENSES_KEY in self.filehandler.paths:
            self.show_popup('Expenses')
            return

        if not self.INVENTORY_KEY in self.filehandler.paths:
            msg = CTkMessagebox(title='Warning', message='Previous retail inventory file not selected. Manual changes will not carry over to new file', icon='warning', option_1='Continue', option_2='Cancel')
            response = msg.get()

            if response=='Cancel':
                return

        self.filehandler.select_directory(self.OUTPUT_KEY)

        if not self.OUTPUT_KEY in self.filehandler.paths:
            return

        inventory = FileIO.read_file(self.filehandler.paths[ self.PRODUCTS_KEY ])
        expenses = FileIO.read_file(self.filehandler.paths[ self.EXPENSES_KEY ])


        inventory = DataTransform.clean_inventory(inventory)
        expenses = DataTransform.clean_expenses(expenses)

        retail_inventory = ReportHandler.create_retail_inventory(inventory, expenses)
        
        if self.INVENTORY_KEY in self.filehandler.paths:
            old_retail_inventory = FileIO.read_file(self.filehandler.paths[ self.INVENTORY_KEY ], no_strip=True)
            ReportHandler.copy_manual_fields(retail_inventory, old_retail_inventory)
        
        FileIO.write_file(retail_inventory, self.filehandler.paths[ self.OUTPUT_KEY ].name)
        
        del self.filehandler.paths[ self.OUTPUT_KEY ]


app = App()
app.mainloop()
