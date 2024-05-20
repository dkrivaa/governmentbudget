import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from general import general_functions

# Opening workbook
book, available_years = general_functions.openGoogle()
# Ministry codes for the various orgs in ministry (column index 9) - returns list with lists of codes
ministry_codes = general_functions.mops_codes()
# wage codes - columns index 15 and 17 - returns list of codes
wage_codes = general_functions.wage_codes()
# budget types - returns list of lists of codes
types = general_functions.budget_types()

# making dataframe with all mops data for all years
df = get_as_dataframe(book.worksheet('mops'))

df_ministry = df[df.iloc[:, 9].isin(ministry_codes[0])]
df_witness = df[df.iloc[:, 9].isin(ministry_codes[1])]
df_police = df[df.iloc[:, 9].isin(ministry_codes[2])]
df_prison = df[df.iloc[:, 9].isin(ministry_codes[3])]
df_fire = df[df.iloc[:, 9].isin(ministry_codes[4])]

df_list = [df_ministry, df_witness, df_police, df_prison, df_fire]

for data in df_list:
    budget = data.iloc[:, 22].sum()
    print(budget)

# budget_sums = [(year, budget_type, data[(data.iloc[:, 0] == year) &
#                                         (data.iloc[:, 21] == budget_type)].iloc[:, 22].sum())
#                for data in df_list
#                for year in available_years
#                for budget_type in types]
#
# print(budget_sums)




