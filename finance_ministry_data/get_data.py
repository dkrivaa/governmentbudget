import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gspread_dataframe import get_as_dataframe, set_with_dataframe
import pandas as pd
import requests
from io import BytesIO

from general import general_functions


# Getting the raw data from Excel files
def make_Google_sheets(url):
    try:
        # Getting data from url
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            # Wrap the byte string in a BytesIO object
            excel_buffer = BytesIO(response.content)
            # Make dataframe
            df = pd.read_excel(excel_buffer)

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

            name = url[-9:-5]

            return name, df
    except Exception as e:
        print("Error occurred:", e)
        return None


def make_Google_sheets_2024(file):
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

        if file == 'before0710original2024.xlsx':
            name = 20241
        else:
            name = 2024

        return name
    except Exception as e:
        print("Error occurred:", e)
        return None


# Opening the workbook
book = general_functions.openGoogle()

# url for Excel data from Finance Ministry
# These url were taken from 'https://www.gov.il/he/departments/policies/tableau'
# url2024 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2024.xls'
url2023 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2023.xlsx'
url2022 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2022.xlsx'
url2021 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_tableau_BudgetData2021.xlsx'
url2020 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2020.xlsx'
url2019 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2019.xlsx'
url2018 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2018.xlsx'
url2017 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2017.xlsx'
url2016 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2016.xlsx'
url2015 = 'https://www.gov.il/BlobFolder/policy/tableau/he/tableau_BudgetData2015.xlsx'
# url20241 = 'C:\\Users\danny\Desktop\BudgetData\original2024Before0710231024.xlsx'

url_list = [url2015, url2016, url2017, url2018, url2019, url2020, url2021, url2022, url2023]
files = ['before0710original2024.xlsx', 'new2024.xlsx']

for url in url_list:
    name = make_Google_sheets(url)
    print(name)
    # book.add_worksheet(title=name, rows=len(df)+1, cols=len(df.columns)+1)
    # set_with_dataframe(book.name, df)


# for file in files:
#     name, df = make_Google_sheets_2024(file)
#     book.add_worksheet(title=name, rows=len(df) + 1, cols=len(df.columns) + 1)
#     set_with_dataframe(book.name, df)

