import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from general import general_functions

# Opening workbook
book, available_years = general_functions.openGoogle()
# Ministry codes for the various orgs in ministry (column index 9)
ministry_codes = general_functions.mops_codes()
# wage codes - columns index 15 and 17
wage_codes = general_functions.wage_codes()

# making dataframe with all mops data for all years
df = get_as_dataframe(book.worksheet('mops'))
print(len(df))





