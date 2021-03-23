import pandas as pd
gl = pd.read_csv('G:\DataA\game_logs.csv', nrows=5)
# gl = pd.read_csv('G:\DataA\game_logs.csv', nrows=5) # удобно для того, чтобы показать 5 строк

# Начнём со среднего показателя использования памяти по разным типам данных.
for dtype in ['float', 'int', 'object']:
    selected_dtype = gl.select_dtypes(include=[dtype])
    mean_usage_b = selected_dtype.memory_usage(deep=True).mean()
    mean_usage_mb = mean_usage_b / 1024 ** 2
    print("Average memory usage for {} columns: {:03.2f} MB".format(dtype, mean_usage_mb))

# Мы будем часто выяснять то, сколько памяти используется,
# поэтому создадим функцию, которая поможет нам сэкономить немного времени.


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:  # исходим из предположения о том, что если это не DataFrame, то это Series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2  # преобразуем байты в мегабайты
    return "{:03.2f} MB".format(usage_mb)


# Перевод int и float в данные 8 бит
gl_int = gl.select_dtypes(include=['int'])
converted_int = gl_int.apply(pd.to_numeric, downcast='unsigned')

print(mem_usage(gl_int))
print(mem_usage(converted_int))

compare_ints = pd.concat([gl_int.dtypes, converted_int.dtypes], axis=1)
compare_ints.columns = ['before', 'after']
compare_ints.apply(pd.Series.value_counts)

gl_float = gl.select_dtypes(include=['float'])
converted_float = gl_float.apply(pd.to_numeric, downcast='float')

print(mem_usage(gl_float))
print(mem_usage(converted_float))

compare_floats = pd.concat([gl_float.dtypes, converted_float.dtypes], axis=1)
compare_floats.columns = ['before', 'after']
compare_floats.apply(pd.Series.value_counts)

optimized_gl = gl.copy()

optimized_gl[converted_int.columns] = converted_int
optimized_gl[converted_float.columns] = converted_float

print(mem_usage(gl))
print(mem_usage(optimized_gl))

gl_obj = gl.select_dtypes(include=['object']).copy()
gl_obj.describe()

# Создадим цикл, который перебирает все столбцы, хранящие данные типа object,
# выясняет, не превышает ли число уникальных значений в столбцах 50%, и если это так, преобразует их в тип category.

converted_obj = pd.DataFrame()

for col in gl_obj.columns:
    num_unique_values = len(gl_obj[col].unique())
    num_total_values = len(gl_obj[col])
    if num_unique_values / num_total_values < 0.5:
        converted_obj.loc[:, col] = gl_obj[col].astype('category')
    else:
        converted_obj.loc[:, col] = gl_obj[col]

# Срывнить использование памяти до и после.
print(mem_usage(gl_obj))
print(mem_usage(converted_obj))

compare_obj = pd.concat([gl_obj.dtypes, converted_obj.dtypes], axis=1)
compare_obj.columns = ['before',  'after']
compare_obj.apply(pd.Series.value_counts)

# Можно вспомнить, что исходные данные были представлены в целочисленном виде и уже оптимизированы с использованием
# типа uint32. Из-за этого преобразование этих данных в тип datetime приведёт к удвоению потребления памяти, так как
# этот тип использует для хранения данных 64 бита. Однако в преобразовании данных к типу datetime, всё равно, есть смысл
# , так как это позволит нам легче выполнять анализ временных рядов.
# Преобразование выполняется с использованием функции to_datetime(), параметр format которой указывает на то, что данные
# хранятся в формате YYYY-MM-DD.

date = optimized_gl.date
optimized_gl['date'] = pd.to_datetime(date, format='%Y%m%d')

print(mem_usage(optimized_gl))

gl.head()