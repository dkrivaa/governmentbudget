import base64
import gspread
from google.oauth2.service_account import Credentials
import os
import json


# Function that goes at beginning of python script run by GitHub action and opens the
# workbook
def openGoogle():
    credentials_json_string = os.environ.get('credentials_json_string')
    credentials_json = json.loads(base64.b64decode(credentials_json_string))
    sheet_id = os.environ.get('sheet_id')

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_info(credentials_json, scopes=scopes)
    client = gspread.authorize(creds)

    book = client.open_by_key(sheet_id)

    # making list of sheets with 'raw data' from Finance Ministry
    sheets_list = book.worksheets()
    available_years = []
    for sheet in sheets_list:
        try:
            name = int(sheet.title)
            available_years.append(str(name))
        except ValueError:
            pass

    # clear result sheet
    book.worksheet('results').clear()

    # return the workbook and list of available years
    return book, available_years


def mops_codes():
    # mops codes for column index = 9
    ministry_codes = [[750, 5230], [755], [780, 5250], [770, 5240], [760]]
    return ministry_codes

def wage_codes():
    # general wage codes - column index 15, column index 17,
    wage = [1, 30]

