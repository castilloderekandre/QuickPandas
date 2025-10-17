import pandas as pd

class FileIO:
    def read_file(self, path: str):
        df = pd.read_excel(path)
        return df

    def write_file(self, df: pd.DataFrame, path: str):
        df.to_excel(path)
