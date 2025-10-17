import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

import re
import math
import numpy as np
import customtkinter as ctk

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

    def main(self):
        self.retail_inventory = pd.DataFrame(
            {
                'LAST 6 OF VIN': [], 
                'YEAR': [], 
                'MAKE': [], 
                'MODEL': [], 
                'MILEAGE': [], 
                'LOCATION': [], 
                'INVENTORY ($)': [], 
                'EXPENSES ($)': [], 
                'TOTAL INVESTED ($)': [], 
                'MISC.': [], 
                'SOURCED FROM': [], 
                'SRP ($)': [], 
                'DATE RECEIVED': [], 
                'OPEN INVOICE?': [], 
                'AGE': []
            })


        expenses = pd.read_excel(self.filehandler.paths[self.EXPENSES_KEY])
        products_and_services = pd.read_excel(self.filehandler.paths[self.PRODUCTS_KEY])

        products = products_and_services.loc[products_and_services.Type == 'Inventory', ['Product/Service Name', 'Sales Description', 'SKU', 'Sales Price / Rate', 'Purchase Cost']]

        expenses = expenses.loc[[3, 9, 10, 11]]
        expenses = expenses.T
        expenses.columns = expenses.iloc[0]
        expenses = expenses[1:-1]
        expenses.set_index('Distribution account', inplace=True)

        def clean_index(index):
            return str(index).split('.')[0]

        expenses.index = expenses.index.map(clean_index)

        expenses.fillna(0, inplace=True)
        expenses = expenses.infer_objects(copy=False)

        self.create_retail_report(products, expenses)
        
        if self.INVENTORY_KEY in self.filehandler.paths:
            old_retail_inventory = pd.read_excel(self.filehandler.paths[self.INVENTORY_KEY])
            self.update_retail_inventory(old_retail_inventory)

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

        self.main()
        
        self.retail_inventory.to_excel(self.filehandler.paths[self.OUTPUT_KEY].name)


app = App()
app.mainloop()
