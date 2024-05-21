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

# Get the value of the ORGANIZATION argument
organization_code = sys.argv[1]

organization = 'ministry'
if organization_code is not None:
    organization_list = ['ministry', 'witness', 'police', 'prison', 'fire']
    organization = organization_list[int(organization_code)-1]
    print('organization', organization)

else:
    print('code not passed')

# # Opening workbook
# book, available_years = general_functions.openGoogle()
# # Ministry codes for the various orgs in ministry (column index 9) - returns list with lists of codes
# ministry_codes = general_functions.mops_codes()
# # wage codes - columns index 15 and 17 - returns list of codes
# wage_codes = general_functions.wage_codes()
# # budget types - returns list of lists of codes
# types = general_functions.budget_types()
#
# # making dataframe with all mops data for all years
# df = get_as_dataframe(book.worksheet('mops'))


