import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
# from gspread_formatting import *

from general import general_functions
import itertools

# Opening workbook
book, available_years = general_functions.openGoogle()

df_2024 = get_as_dataframe(book.worksheet('2024'))

column_1 = df_2024.columns[1]
column_2 = df_2024.columns[2]

# Get unique pairs of values from 'column1' and 'column2'
unique_pairs = df_2024[['column_1', 'column_2']].drop_duplicates()

# Convert to list of tuples if needed
macro_codes_list = list(unique_pairs.itertuples(index=False, name=None))
print(macro_codes_list)

