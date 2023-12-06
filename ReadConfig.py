import json


# Method to read config file settings
def read_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
        return config


# config = read_config()
# print(config['ExcelSettings']['excelFilePath'])
# print(config['FilePaths']['ExcelFilePath'])