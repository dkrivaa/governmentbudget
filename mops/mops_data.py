import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from general import general_functions

# Opening workbook
book, available_years = general_functions.openGoogle()

mops_df = pd.DataFrame
# Extracting mops data for each year
for year in available_years:
    sheet = book.worksheet(year)
    df = pd.DataFrame(sheet.get_all_records())
    temp_df = df[df.iloc[:, 3] == '12']

    mops_df = pd.concat([mops_df, temp_df], ignore_index=True)

# Make MOPS worksheet in Google file
try:
    if book.worksheet('mops'):
        book.del_worksheet(book.worksheet('mops'))
except gspread.exceptions.WorksheetNotFound:
    pass

book.add_worksheet(title='mops', rows=len(mops_df) + 1, cols=len(mops_df.columns) + 1)
set_with_dataframe(book.worksheet('mops'), mops_df)