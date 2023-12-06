import pandas as pd
import pyodbc

# import sqlalchemy as sa
# from sqlalchemy import create_engine
# import urllib

import ReadConfig

config = ReadConfig.read_config()

excelFilePath = config['ExcelSettings']['excelFilePath']

DRIVER = config['DatabaseConnection']['DRIVER']
SERVER = config['DatabaseConnection']['SERVER']
DATABASE = config['DatabaseConnection']['DATABASE']
USERNAME = config['DatabaseConnection']['USERNAME']
PASSWORD = config['DatabaseConnection']['PASSWORD']



try:
    connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};User ID={USERNAME};Password={PASSWORD}'
    connection = pyodbc.connect(connectionString)

    dataframe = pd.read_excel(excelFilePath, engine='openpyxl')
    dataframe.columns = dataframe.columns.str.replace(' ' , '')
   

    columns = ",".join(f"[{col}]" for col in dataframe.columns)
    columnsCount = len(dataframe.columns)
    columnsValues = ",".join("?" for _ in range(columnsCount))

    # Filter rows with valid datetime values in the datetime column
    df = dataframe[pd.to_datetime(dataframe['LastLogon'], errors='coerce').notnull()]


    if df.empty:
        print("No valid datetime values found in the specified column.")
    else:
        cursor = connection.cursor()
        
        # Insert the DataFrame into the SQL Server table
        for index, row in df.iterrows():
            insert_query = f'INSERT INTO [CPDBA_USER_GROUP_tab] ({columns}) VALUES ({columnsValues});'
            cursor.execute(insert_query, tuple(row))


        connection.commit()
        cursor.close()
        # connection.close()


except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'connection' in locals():
        connection.close()

#print(dataframe)