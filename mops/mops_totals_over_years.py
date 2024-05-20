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

# Splitting dataframe into individual organizations dataframes
df_ministry = df[df.iloc[:, 9].isin(ministry_codes[0])]
df_witness = df[df.iloc[:, 9].isin(ministry_codes[1])]
df_police = df[df.iloc[:, 9].isin(ministry_codes[2])]
df_prison = df[df.iloc[:, 9].isin(ministry_codes[3])]
df_fire = df[df.iloc[:, 9].isin(ministry_codes[4])]

df_list = [df_ministry, df_witness, df_police, df_prison, df_fire]
index_list = list(range(len(df_list)))  # Create a list of indices for df_list

# getting list of lists (index (of org df in df_list), year, budget_type, sum of total budget)
total_budget_sums = [[index + 1, year, budget_type,
                      data[(data.iloc[:, 0] == int(year)) &
                           (data.iloc[:, 21] == budget_type)].iloc[:, 22].sum()]
                     for index, data in zip(index_list, df_list)
                     for year in available_years
                     for budget_type in types]


# getting list of lists (index (of org df in df_list), year, budget_type, sum of total wages)
total_wage_sums = []

for index, data in enumerate(df_list):
    for year in available_years:
        for budget_type in types:
            # Convert year to int for comparison
            year = int(year)

            # Filter rows based on conditions
            filtered_data = data[(data.iloc[:, 0] == year) &
                                 (data.iloc[:, 21] == budget_type) &
                                 ((data.iloc[:, 15].isin(wage_codes)) |
                                  (data.iloc[:, 17].isin(wage_codes)))]

            # Check if any rows matched the conditions
            if not filtered_data.empty:
                # Sum the values in column 22
                wage_sum = filtered_data.iloc[:, 22].sum()
                # Append to total_wage_sums list along with the index
                total_wage_sums.append([index + 1, year, budget_type, wage_sum])

# Calculating totals for all orgs
totals = [[0, year, budget_type, sum(inner_list[3] for inner_list in total_budget_sums if
            inner_list[1] == year and inner_list[2] == budget_type)]
            for year in available_years
            for budget_type in types]

# calculating wages for all orgs
wages = [[0, year, budget_type, sum(inner_list[3] for inner_list in total_budget_sums if
            inner_list[1] == year and inner_list[2] == budget_type)]
            for year in available_years
            for budget_type in types]


# Combining the totals and the wages
totals += total_budget_sums
wages += total_wage_sums

# Calculating the rest of budget (total - wages)
other = []

for inner_list1 in totals:
    for inner_list2 in wages:
        if inner_list1[:3] == inner_list2[:3]:  # Check if first, second, and third elements are identical
            other.append([inner_list1[0],
                          inner_list1[1],
                          inner_list1[2],
                          inner_list1[3] - inner_list2[3]])
        else:
            other.append([inner_list1[0],
                          inner_list1[1],
                          inner_list1[2],
                          999])

print('totals', totals)
print('wages', wages)
print('other', other)




