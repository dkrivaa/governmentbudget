import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
# from gspread_formatting import *

from general import general_functions

# Opening workbook
book, available_years = general_functions.openGoogle()

df_2024 = get_as_dataframe(book.worksheet('2024'))
# setting dataframe column names
column_1 = df_2024.columns[1]
column_2 = df_2024.columns[2]
column_3 = df_2024.columns[3]
column_4 = df_2024.columns[4]
column_21 = df_2024.columns[21]  # type of budget (original, approved, executed)
column_22 = df_2024.columns[22]  # net budget

level1_budgets = [[group[0], group[1],
                    group_df.loc[group_df[column_21] == 'מקורי', column_22].sum()]
                    for group, group_df in df_2024.groupby([column_1, column_2])]

print('macro_budgets', level1_budgets)

level2_budgets = [[group[0], group[1], group[2], group[3],
                    group_df.loc[group_df[column_21] == 'מקורי', column_22].sum()]
                    for group, group_df in df_2024.groupby([column_1, column_2, column_3, column_4])]

print('level2_budgets', level2_budgets)

# writing results to google sheet
sheet = book.worksheet('results')
sheet.append_rows(level1_budgets)
sheet.format('C', {'numberFormat': {'type': 'NUMBER', 'pattern': '#,###'}})
sheet.append_rows(level2_budgets)
sheet.format('E', {'numberFormat': {'type': 'NUMBER', 'pattern': '#,###'}})
