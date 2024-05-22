import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
# from gspread_formatting import *

from general import general_functions
from game import macro_assumptions

# Opening workbook
book, available_years = general_functions.openGoogle()
# Get the value of the year argument chosen by user
year = sys.argv[1]


def macro_for_year(year):
    year = str(year)
    df = get_as_dataframe(book.worksheet(year))
    # setting dataframe column names
    column_1 = df.columns[1]
    column_2 = df.columns[2]
    column_3 = df.columns[3]
    column_4 = df.columns[4]
    column_21 = df.columns[21]  # type of budget (original, approved, executed)
    column_22 = df.columns[22]  # net budget

    level1_budgets = [[group[0], group[1],
                        group_df.loc[group_df[column_21] == 'מקורי', column_22].sum()]
                        for group, group_df in df.groupby([column_1, column_2])]
    df_level1 = pd.DataFrame(level1_budgets, columns=['code1', 'area1', f'budget{year}'])

    level2_budgets = [[group[0], group[1], group[2], group[3],
                        group_df.loc[group_df[column_21] == 'מקורי', column_22].sum()]
                        for group, group_df in df.groupby([column_1, column_2, column_3, column_4])]
    df_level2 = pd.DataFrame(level2_budgets, columns=['code1', 'area1', 'code2', 'area2', f'budget{year}'])

    df_level2['code'] = df_level2['code1'] + df_level2['code2']




    # writing results to google sheet
    # sheet = book.worksheet('results')
    # set_with_dataframe(sheet, df_level1)
    # sheet.format('C', {'numberFormat': {'type': 'NUMBER', 'pattern': '#,###'}})
    # set_with_dataframe(sheet, df_level2, row=11, col=1)
    # sheet.format('E', {'numberFormat': {'type': 'NUMBER', 'pattern': '#,###'}})

macro_for_year(year)


