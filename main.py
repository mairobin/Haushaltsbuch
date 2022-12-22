import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys
import pandas
import numpy
import json
import argparse

from pathlib import Path

from datetime import datetime

from Kategorien import CATEGORIES
from Kategorien import pretty_print_categories

def split_df(df):
    # Splits records in income, expenses and paypal
    df_paypal = df_income = df_expenses = pandas.DataFrame(columns=df.columns)

    for index, row in df.iterrows():

        # ING uses Format 111.111,55 €
        # This must be changed for proper processing in Python
        betrag = str(row['Betrag']).replace('.','')
        betrag = str(betrag).replace(',','.')

        # Collect all Paypal records in specific dataframe
        if str(row['Auftraggeber/Empfänger']).lower().find('paypal') != -1:
            df_paypal = df_paypal.append(row, ignore_index=True)
        # Collect all earnings
        elif float(betrag) > 0:
            df_income = df_income.append(row, ignore_index=True)
        # Collect all expenses
        elif float(betrag) <= 0:
            df_expenses = df_expenses.append(row, ignore_index=True)

    return df_income, df_expenses, df_paypal

def check_number_of_records(num_records, num_records_full_df):
    sum(num_records)
    if num_records_full_df != sum(num_records):
        raise ValueError("Different count of records in sub dataframes than in the original")

def _get_category_from_user(df, row):
    row_as_df = pandas.DataFrame(columns=df.columns)
    row_as_df = row_as_df.append(row)
    print()
    print(row_as_df.to_string())
    print()
    print('Welcher Kategorie soll diese Transaktion zugeordnet werden?')
    pretty_print_categories()
    category = str(input("Gebe Kategorie ein: "))
    return category

def is_cash(identifier):
    if str(identifier).startswith("Bargeldauszahlung"):
        return "Unzurechenbare Barzahlungen"


def _find_category(history, identifier):
    # Entferne VISA da es bei Visa Abhebungen vorangestellt wird
    if identifier.startswith('VISA '):
        identifier = identifier.replace("VISA ", "")

    # If Cash
    if str(identifier).startswith("Bargeldauszahlung"):
        category = "Unzurechenbare Barzahlungen"

    # Lookup in history
    category = history.get(identifier)
    return category

def _add_to_history(history, identifier, category):
    print("Soll der Eintrag {0} mit der Kategorie {1} der Historie hinzugefügt werden?")
    to_add = False
    if str(input("y / n: ")).lower() == "y":
        to_add = True
        if identifier.startswith("VISA "):
            identifier = identifier.replace("VISA ", "")
    if to_add:
        history[identifier] = category

def categorize(df, history):

    categorized_df = df.copy()

    for index, row in df.iterrows():
        identifier = str(row['Auftraggeber/Empfänger'])

        category = _find_category(history, identifier)

        if category:
            categorized_df.at[index, 'Kategorie'] = category

        else:
            category = _get_category_from_user(df, row)
            categorized_df.at[index, 'Kategorie'] = CATEGORIES[category]

            _add_to_history(history, identifier, category)


    return categorized_df, history

def drop_records_not_from_period(df):
    # Find the respective Period to process
    res = df.loc[df['Buchungstext'] == "Gehalt/Rente"]
    indices = list(res.index)

    if len(indices) > 1:
        print("Moechtest du Ereignisse ausserhalb des letzten Berichtszeitraum ignorieren?")
        i= str(input("y/n: "))

        if i == 'y':
            new = indices[0]
            old = indices[1]

            df = df.iloc[new:old]

    return df



def drop_unnecessary_columns(df):
    print(df.head(1).to_string())

    cols = str(input("Specify Columns to Drop from 1 to n comma-seperated. Eg. '1,5,6': "))
    if not cols:
        return
    cols = cols.split(',')
    to_delete = list()
    for c in cols:
        col = int(c)
        col = col - 1
        to_delete.append(col)
    df.drop(df.columns[to_delete], axis=1, inplace=True)

def get_history_from_file(filepath):
    with open(filepath, 'r') as f:
        history = json.load(f)
    return history

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='Haushaltsplan Kategorisierung',
        description='Hilft bei der Kategorisierung des haushaltsplans')
    parser.add_argument('filename')  # positional argument
    parser.add_argument('history')  # positional argument
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    # Parse Filepaths of CSV File and History
    args = parse_arguments()
    csv = args.filename
    history_filename = args.history


    # Read csv and add Category
    df = pandas.read_csv(csv, encoding='latin-1', delimiter=";")
    df = df.assign(Kategorie=str(""))

    # Drop unnecessary colums
    drop_unnecessary_columns(df)

    # Find Period of Investigation
    df = drop_records_not_from_period(df)

    history = get_history_from_file(history_filename)

    df_categorized, updated_history = categorize(df, history)

    output_file = history_filename + "_" + str(datetime.now().strftime("%m_%d_%Y_%H_%M"))
    with open(output_file, 'w') as json_file:
        json.dump(updated_history, json_file)

    o = 'Kontoauszug_kategorisiert_' + str(datetime.now().strftime("%m_%d_%Y")) + '.xlsx'
    with pandas.ExcelWriter(o) as writer:
        df_categorized.to_excel(writer, sheet_name=datetime.now().strftime("%m_%d_%Y"))

    print("Job Done. Have a look at the Output Excelfile")