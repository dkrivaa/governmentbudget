import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
import numpy as np
from gspread_dataframe import get_as_dataframe, set_with_dataframe
# from gspread_formatting import *

from general import general_functions
import itertools


# Check if the command-line argument is provided
if len(sys.argv) < 2:
    print("Usage: python mops_organization_budget.py ORGANIZATION")
    sys.exit(1)

# Get the value of the ORGANIZATION argument chosen by user
organization_code = sys.argv[1]

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
# Keeping only data for organization chosen
df = df[df.iloc[:, 9].isin(ministry_codes[int(organization_code)])]
# Getting names of columns
column_0 = df.columns[0]
column_13 = df.columns[13]
column_14 = df.columns[14]
column_21 = df.columns[21]
column_22 = df.columns[22]

# Making list of lists for takanot
takanot_budget = [[list(group),
                    group_df.loc[group_df[column_21] == 'מקורי', column_22],
                    group_df.loc[group_df[column_21] == 'מאושר', column_22],
                    group_df.loc[group_df[column_21] == 'ביצוע', column_22]]
                    for group, group_df in df.groupby([column_13, column_0, column_14])]

print(takanot_budget)

# # Making list of lists of programs (tochniot)
# program_budgets = [[list(group),
#                     group_df.loc[group_df[column_21] == 'מקורי', column_22].sum(),
#                     group_df.loc[group_df[column_21] == 'מאושר', column_22].sum(),
#                     group_df.loc[group_df[column_21] == 'ביצוע', column_22].sum()]
#                     for group, group_df in df.groupby([column_11, column_0, column_12])]
#
# # Making array of arrays for table
# table_data = []
# for program_item in program_budgets:
#     flattened_list = []
#     for sublist in program_item:
#         if isinstance(sublist, list):
#             for item in sublist:
#                 if isinstance(item, np.int64):  # Check if the item is of type int64
#                     flattened_list.append(int(item))  # Convert it to a standard Python int
#                 else:
#                     flattened_list.append(item)
#         else:
#             if isinstance(sublist, np.int64):  # Check if the item is of type int64
#                 flattened_list.append(int(sublist))  # Convert it to a standard Python int
#             else:
#                 flattened_list.append(sublist)
#     table_data.append(flattened_list)

# writing results to google sheet
# sheet = book.worksheet('results')
# sheet.append_rows(table_data)
# sheet.format('D:F', {'numberFormat': {'type': 'NUMBER', 'pattern': '#,###'}})
