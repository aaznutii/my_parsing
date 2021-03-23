import pandas as pd
data_original = pd.read_csv('G:\DataA\demografy\dem_data.csv')
data_copy = data_original.copy()
# data_int = data_copy.select_dtypes(include=['int'])
# data_float = data_copy.select_dtypes(include=['float'])
# converted_int = data_int.apply(pd.to_numeric, downcast='unsigned')
# converted_float = data_float.apply(pd.to_numeric, downcast='unsigned')

print(data_copy)