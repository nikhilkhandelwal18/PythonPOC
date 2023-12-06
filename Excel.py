import pandas as pd

import ReadConfig

config = ReadConfig.read_config()
print(config['ExcelSettings']['excelFilePath'])

excelFilePath = config['ExcelSettings']['excelFilePath']

# dataframe1 = pd.read_excel(r'C:\Test\CPDBA_USER_GROUP_tab.xlsx')
# dataframe = pd.read_excel(r'C:\Local Data\CPDBA_USER_GROUP_tab.xlsx', engine='openpyxl')

dataframe = pd.read_excel(excelFilePath, engine='openpyxl')

# print(dataframe)

print('number of rows and columns in the dataset', dataframe.shape)
print('number of rows in the dataset', len(dataframe))
print('name of the columns in the dataset', dataframe.columns)
print(",".join(f"[{col}]" for col in dataframe.columns))

 