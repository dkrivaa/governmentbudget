import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd

from general import general_functions

# Opening workbook
book, available_years = general_functions.openGoogle()

for year in available_years:
    sheet = book.worksheet(year)
    df = pd.DataFrame(sheet.get_all_records())
    print(len(df))
