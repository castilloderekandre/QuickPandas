class DataTransform:
    def parse_description(self, description):
        schema_elements = []
        for identifier in self.schema:
            description = str(description)
            index = description.find(identifier) 

            if (index == -1):
                schema_elements.append('Incorrect Schema')
                continue

            index += len(identifier) + 1

            end_index = description.find('\n', index)

            if (end_index == -1):
                end_index = len(description)
            
            schema_elements.append(description[index:end_index])

        return schema_elements

    def parse_product_name(self, name):
        breakdown = []
        pattern = r":(\d+)\s+(\w+)\s+(.+)\(VIN#.+\)"
        capture_groups = re.search(pattern, name)
        if capture_groups:
            breakdown.extend(list(capture_groups.groups()))
        else:
            breakdown = ['-', '-', '-']
            
        return breakdown

    def parse_product(self, index, product, expenses):
        vin = product.SKU[-6:]
        inventory = product['Purchase Cost']
        expenses = sum(expenses.loc[vin])
        product_series = [
            vin, # LAST 6 OF VIN
            *self.parse_product_name(product['Product/Service Name']), # YEAR, MAKE, MODEL
            *self.parse_description(product['Sales Description']), # MILEAGE (BASED ON SCHEMA)
            None, # LOCATION
            inventory, # INVENTORY
            expenses, # EXPENSES
            inventory + expenses, # TOTAL INVESTED
            None, # MISC
            None, # SOURCED FROM
            product['Sales Price / Rate'], # SRP
            None, # DATE RECEIVED
            None, # OPEN INVOICE
            f'=TODAY() - N{index+2}', # AGE
        ]

        return product_series
