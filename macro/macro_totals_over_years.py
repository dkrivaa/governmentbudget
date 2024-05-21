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

