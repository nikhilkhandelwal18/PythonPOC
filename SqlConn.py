import pymssql

connectionString = 'Driver=SQL Server;Server=AWSVAMFRRDS01D.njt.gov;Database=mf_config;Trusted_Connection=yes;'

conn = pymssql.connect(connectionString)

# conn = pymssql.connect('AWSVAMFRRDS01D.njt.gov', user, password, "tempdb")
cursor = conn.cursor(as_dict=True)

cursor.execute("""'SELECT distinct 'BREV' as AppName, BRSF_USER_ID as USER_ID  FROM[db230].[dbo].[BREV_SECURTY_FL] WHERE TRIM(BRSF_USER_ID) != '';""")

for row in cursor:
      print(f"{row.AppName}\t{row.USER_ID}\t")

conn.close()