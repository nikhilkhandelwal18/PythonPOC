import pandas as pd
import pyodbc

import ReadConfig

config = ReadConfig.read_config()

excelFilePath = config['FilePaths']['ExcelFilePath']
connectionString = config['ConnectionStrings']['MFDatabase']

try:
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
        
        print("Inserting into database : ")

        # Insert the DataFrame into the SQL Server table <.head(1)>
        for index, row in df.iterrows():
            insert_query = f'INSERT INTO [CPDBA_USER_GROUP_tab] ({columns}) VALUES ({columnsValues});'
            cursor.execute(insert_query, tuple(row))
            print("Row #", index)


        connection.commit()
        cursor.close()
        # connection.close()
        
        print("Complete")
        
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    #if 'connection' in locals():
    connection.close()

#print(dataframe)