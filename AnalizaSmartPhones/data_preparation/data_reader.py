import pandas as pd

def readData(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Data read successfully form file: ", file_path)
        return data
    except Exception as ex:
        print("Error reading data from file: ", file_path)
        print("Error: ", ex)
        return None