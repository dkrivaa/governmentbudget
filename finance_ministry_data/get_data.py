import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gspread
import pandas as pd
import requests
from io import BytesIO


# Getting the raw data from Excel files and returning list with nested lists of dataframes
# each nested list, representing specific year, consist of 5 dataframes - one for each organization
def makeFile():
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

    for url in url_list:

        response = requests.get(url)
        if response.status_code == 200:

            # Wrap the byte string in a BytesIO object
            excel_buffer = BytesIO(response.content)
            # Make dataframe
            df = pd.read_excel(excel_buffer)

            # change name of net budget column
            df = df.rename(columns={'הוצאה נטו': 'netBudget'})
            df = df.rename(columns={'סוג תקציב': 'budgetType'})

            # make budget sums into numbers
            # Step 1: Replace values in the format (20) with the corresponding negative value
            df['netBudget'] = df['netBudget'].replace(r'\((.*?)\)', r'-\1', regex=True)

            # Step 2: Replace '-' with 0
            df['netBudget'] = df['netBudget'].replace('-', '0', regex=False)

            # Step 3: Replace NaN values with 0
            df['netBudget'] = df['netBudget'].fillna('0')

            # Convert to integers
            df['netBudget'] = df['netBudget'].astype(float)

            # Drop unnecessary columns
            columnsToDrop = [3, 6, 11, 14, 17, 20, 23, 26]
            df = df.drop(df.columns[columnsToDrop], axis=1)

            name = url[-9:-5]
            df.to_excel(f'{name}.xlsx')


def makeFiles2024():
    files = ['before0710original2024.xlsx', 'new2024.xlsx']

    for file in files:
        # Make dataframe
        df = pd.read_excel(file)

        # change name of net budget column
        df = df.rename(columns={'הוצאה נטו': 'netBudget'})
        df = df.rename(columns={'סוג תקציב': 'budgetType'})

        # make budget sums into numbers
        # Step 1: Replace values in the format (20) with the corresponding negative value
        df['netBudget'] = df['netBudget'].replace(r'\((.*?)\)', r'-\1', regex=True)

        # Step 2: Replace '-' with 0
        df['netBudget'] = df['netBudget'].replace('-', '0', regex=False)

        # Step 3: Replace NaN values with 0
        df['netBudget'] = df['netBudget'].fillna('0')

        # Convert to integers
        df['netBudget'] = df['netBudget'].astype(float)

        # Drop unnecessary columns
        columnsToDrop = [3, 6, 11, 14, 17, 20, 23, 26]
        df = df.drop(df.columns[columnsToDrop], axis=1)

        if file == files[0]:
            name = 20241
        else:
            name = 2024

        df.to_excel(f'{name}.xlsx')

