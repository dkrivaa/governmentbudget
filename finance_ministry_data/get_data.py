import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import pandas as pd

from general import general_functions


# Getting the raw data from Excel files, formatting, dropping unnecessary columns and saving in
# Google sheet
def make_Google_sheets(url):
    try:
        # Make dataframe
        df = pd.read_excel(file)

        # make budget sums into numbers
        # list of columns to re-format
        columns_to_format = [30, 31, 32, 33, 34, 35, 36, 37]
        for column in columns_to_format:
            # Step 1: Replace values in the format (20) with the corresponding negative value
            df[df.columns[column]] = df[df.columns[column]].replace(r'\((.*?)\)', r'-\1', regex=True)
            # Step 2: Replace '-' with 0
            df[df.columns[column]] = df[df.columns[column]].replace('-', '0', regex=False)
            # Step 3: Replace NaN values with 0
            df[df.columns[column]] = df[df.columns[column]].fillna('0')
            # Convert to integers
            df[df.columns[column]] = df[df.columns[column]].astype(float)

        # Drop unnecessary columns
        columnsToDrop = [3, 6, 11, 14, 17, 20, 23, 26]
        df = df.drop(df.columns[columnsToDrop], axis=1)

        if file == files[-1]:
            name = 20241
        else:
            name = file[-9:-5]

        # Correcting year for 20241
        if name == 20241:
            df.iloc[:, 0] = 20241

        return name, df

    except Exception as e:
        print("Error occurred:", e)
        return None


# Opening the workbook
book = general_functions.openGoogle()

files = ['finance_ministry_data/2015.xlsx', 'finance_ministry_data/2016.xlsx',
         'finance_ministry_data/2017.xlsx', 'finance_ministry_data/2018.xlsx',
         'finance_ministry_data/2019.xlsx', 'finance_ministry_data/2020.xlsx',
         'finance_ministry_data/2021.xlsx', 'finance_ministry_data/2022.xlsx',
         'finance_ministry_data/2023.xlsx', 'finance_ministry_data/2024.xlsx',
         'finance_ministry_data/20241.xlsx']

for file in files:
    name, df = make_Google_sheets(file)
    print(name, type(name))
    # if worksheet exist then delete and make new with the same name with updated data
    try:
        if book.worksheet(f'{name}'):
            book.del_worksheet(book.worksheet(f'{name}'))
    except gspread.exceptions.WorksheetNotFound:
        pass

    book.add_worksheet(title=f'{name}', rows=len(df) + 1, cols=len(df.columns) + 1)
    set_with_dataframe(book.worksheet(f'{name}'), df)

