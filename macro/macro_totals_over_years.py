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
column_21 = df_2024.columns[21]
column_22 = df_2024.columns[22]

macro_budgets = [[group[0], group[1],
                    group_df.loc[group_df[column_21] == 'מקורי', column_22].sum()]
                    for group, group_df in df_2024.groupby([column_1, column_2])]

print(macro_budgets)


