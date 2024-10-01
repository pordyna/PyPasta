import scipp as sc
import pandas as pd

def csv_to_dataset(path, mapping='case2params'):
    if mapping == 'case2params':
        df = pd.read_csv(path, index_col='case_index')
        return sc.compat.from_pandas(df, header_parser='bracket')
    if mapping == 'params2case':
        ds = sc.io.load_csv(path, data_columns='case_index', header_parser='bracket')
        return ds['case_index'].group(*ds.coords.keys())
