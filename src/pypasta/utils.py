import scipp as sc
import pandas as pd

def csv_to_dataset(path):
    df = pd.read_csv(path, index_col='case_index')
    return sc.compat.from_pandas(df, header_parser='bracket')
