import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gspread

from general import general_functions

# Opening workbook
book = general_functions.openGoogle()
sheet = book.worksheet('2024')

data = sheet.get_all_values()
print(len(data))