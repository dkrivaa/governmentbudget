import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from general import general_functions

# Opening the workbook
book = general_functions.openGoogle()
# Doing the actual action
book.worksheet('test').update([[1, 2], [3, 4]], 'A1:B2')


