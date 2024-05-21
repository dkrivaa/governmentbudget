import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import gspread
import pandas as pd
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

column_0 = df.columns[0]
column_11 = df.columns[11]
column_12 = df.columns[12]
column_21 = df.columns[21]
column_22 = df.columns[22]

program_names = df[column_12].unique().tolist()
program_numbers = df[column_11].unique().tolist()
print('program_names', len(program_names), program_names)
print('programs numbers', len(program_numbers), program_numbers)

program_budgets = [[list(group),
                    group_df.loc[group_df[column_21] == 'מקורי', column_22].sum(),
                    group_df.loc[group_df[column_21] == 'מאושר', column_22].sum(),
                    group_df.loc[group_df[column_21] == 'ביצוע', column_22].sum()]
                for group, group_df in df.groupby([column_11, column_0])]



print(program_budgets)
