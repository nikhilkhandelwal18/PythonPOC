"""
Connects to a SQL database using pyodbc
"""
import pyodbc

import ReadConfig

config = ReadConfig.read_config()

# DRIVER = 'SQL Server'               #'<drivername>'
# SERVER = 'AWSVAMFRRDS01D.njt.gov'   #'<server-address>'
# DATABASE = 'mf_config'              #'<database-name>'
# USERNAME = 'my_app'                 #'<username>'
# PASSWORD = 'app&*mf'                #'<password>'


DRIVER = config['DatabaseConnection']['DRIVER']
SERVER = config['DatabaseConnection']['SERVER']
DATABASE = config['DatabaseConnection']['DATABASE']
USERNAME = config['DatabaseConnection']['USERNAME']
PASSWORD = config['DatabaseConnection']['PASSWORD']

# connectionString = 'Driver=SQL Server;Server=AWSVAMFRRDS01D.njt.gov;Database=mf_config;Trusted_Connection=yes;'
# connectionString = 'Driver=SQL Server;Server=AWSVAMFRRDS01D.njt.gov;Database=mf_config;User ID=my_app;Password=app&*mf;'
connectionString = f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};User ID={USERNAME};Password={PASSWORD}'

print(connectionString)

conn = pyodbc.connect(connectionString)




def Read_SQL(connection):
    SQL_QUERY = """ SELECT distinct 'BREV' as AppName, BRSF_USER_ID as USER_ID  FROM[db230].[dbo].[BREV_SECURTY_FL] WHERE TRIM(BRSF_USER_ID) != ''; """

    cursor = connection.cursor()
    cursor.execute(SQL_QUERY)

    records = cursor.fetchall()
    for r in records:
        print(f"{r.AppName}\t{r.USER_ID}\t")

Read_SQL(conn)


def Insert_SQL(connection):
    SQL_QUERY = """ INSERT INTO tblPython (Name) VALUES ('Scott') """

    cursor = connection.cursor()
    cursor.execute(SQL_QUERY)

    connection.commit()

    cursor.close()
    connection.close()

    # SQL_QUERY = """ SELECT * FROM tblPython; """

    # cursor = connection.cursor()
    # cursor.execute(SQL_QUERY)

    # records = cursor.fetchall()
    # for r in records:
    #     print(f"{r.AppName}\t{r.USER_ID}\t")


# Insert_SQL(conn)

