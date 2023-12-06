import pyodbc

import ReadConfig

from datetime import datetime

def extract_values(line):
    # BASVBDW 06075Barry D. Woods            1999021620070413BVMSUSR0075
    # BMECJKM103312Joseph K. Marano          2006121320141105BVMSUSR0075
    user_id = line[0:8].strip()
    since = line[8:13].strip()
    name = line[13:39].strip().replace("'", "''")
    mod_dt = line[39:47].strip()
    log_dt = line[47:55].strip()
    group = line[55:63].strip()
    db = line[63:].strip()
    
    return user_id, since, name, mod_dt, log_dt, group, db

def convert_to_date(date_str):
    try:
        # Attempt to parse the date
        date_object = datetime.strptime(date_str, '%Y%m%d')
        return date_object.strftime('%m/%d/%Y')
    except ValueError:
        return None

try:
    config = ReadConfig.read_config()
    input_file_path = config['FilePaths']['TextFilePath']
    # input_file_path = "C:\\Local Data\\CPDBA.SECURITY.MAIN.FRAME.TXT"
    # output_file_path = 'C:\\Local Data\\output_file.txt'

    connectionString = config['ConnectionStrings']['MFDatabase']

    connection = pyodbc.connect(connectionString)
    cursor = connection.cursor()

    with open(input_file_path, 'r') as input_file: #, open(output_file_path, 'w') as output_file:

        header = input_file.readline()  # Skip the header line

        count = 0
           
        for line in input_file:
            count = count + 1
            print("Row #", count)

            if not line:
                break 
        
            user_id, since, name, mod_dt, log_dt, group, db = extract_values(line)
            
            # Convert mod_dt and log_dt to valid date format
            mod_dt = convert_to_date(mod_dt)
            log_dt = convert_to_date(log_dt)
           
            log_dt_formatted = 'null' if log_dt is None else f"'{log_dt}'"
        
            # print(f"User ID: {user_id}, SINCE: {since}, NAME: {name}, MOD DT: {mod_dt}, LOG DT: {log_dt}, GROUP: {group}, DB: {db}")
            # output_file.write(f"User ID: {user_id}, SINCE: {since}, NAME: {name}, MOD DT: {mod_dt}, LOG DT: {log_dt_formatted} , GROUP: {group}, DB: {db}\n")
            insert_query = f"""INSERT INTO [CPDBA_USER_GROUP_tab] ([UserId], [DaySinceLogon], [Name], [LastModified], [LastLogon], [Group], [Database]) 
                                        VALUES ('{user_id}', '{since}', '{name}', '{mod_dt}', {log_dt_formatted}, '{group}', '{db}');"""
            print(insert_query)
            cursor.execute(insert_query)
        
        connection.commit()
        cursor.close()

        print("Complete")
except Exception as e:
    print(f"An error occured: {e}")


# print("Data written to", output_file_path)
