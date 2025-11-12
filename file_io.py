import pandas as pd
from pathlib import Path
from data_transform import DataTransform

class FileIO:
    @classmethod
    def read_file(cls, path: Path, no_strip=False):
        if (path.suffix == '.xls'):
            df = pd.read_excel(path)
            return df
            # pxl.save_as(file_name=path, dest_file_name=path.with_suffix('.xlsx'))
            # path = path.with_suffix('.xlsx')

        if no_strip:
            df = pd.read_excel(path, engine='openpyxl')
            return df

        DataTransform.strip_formulas(path)

        df = pd.read_excel(path, engine='openpyxl')
        return df

    

    @classmethod
    def write_file(cls, df: pd.DataFrame, path: Path):
        df.to_excel(path)
