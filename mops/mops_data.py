import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd

from general import general_functions

# Opening workbook
book = general_functions.openGoogle()
sheet_list = book.worksheets()
print(sheet_list[1])
# sheet = book.worksheet('2024')
#
# df = pd.DataFrame(sheet.get_all_records())
# print(len(df))
