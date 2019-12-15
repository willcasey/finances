import mintapi
import csv
import re
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from lib.functions import *
import pprint


######################################################
#############GLOBAL VARIABLES ########################
SPREADSHEET_NAME = "TRANSACTIONS"
SHEET_NAME = "transactions"


LIB_PATH = "./lib/"
SCOPE = ["https://spreadsheets.google.com/feeds"
        ,'https://www.googleapis.com/auth/spreadsheets'
        ,"https://www.googleapis.com/auth/drive.file"
        ,"https://www.googleapis.com/auth/drive"]
COLS = ['Date', 'Original Description', 'Amount', 'Transaction Type']
CREDS = ServiceAccountCredentials \
         .from_json_keyfile_name('{}client_secret.json'.format(LIB_PATH), SCOPE)
CLIENT = gspread.authorize(CREDS)
print("Creating google sheets api connection")
SPREADSHEET = CLIENT.open(SPREADSHEET_NAME)
SHEET = SPREADSHEET.worksheet(SHEET_NAME)
pp = pprint.PrettyPrinter()
######################################################


def mintParams():
    '''
    concats username and password params
    with default mintparams
    '''
    mintparams = {
        'mfa_method':'sms'
        ,'headless': True
        , 'mfa_input_callback': None
        , 'session_path': None
        , 'imap_account': None
        , 'imap_password': None
        , 'imap_server': None
        , 'imap_folder':'INBOX'
        , 'wait_for_sync': False
        , 'wait_for_sync_timeout': 300
        }
    upw = eval(openFile(path=LIB_PATH, file='password.pw'))
    mintparams.update(upw)
    return mintparams 

def tempTransactions():
    df = pd.read_csv('.temp_transactions.csv', delimiter=",")[:-1]
    df['uuid'] = df[COLS].apply(lambda row: create_sudo_id_field(row), axis=1)
    return df


def sheetsTransactions():
    df = pd.DataFrame(SHEET.get_all_records())
    df['uuid'] = df[COLS].apply(lambda row: create_sudo_id_field(row), axis=1)
    return df 

def joinDFs(mintdf, sheetsdf):
    sheetsdf = sheetsdf[['uuid', 'category']].rename(columns={'uuid': 'sheets_uuid'})
    joindf = mintdf.merge(sheetsdf, how='left', left_on='uuid', right_on='sheets_uuid')
    joindf = joindf[joindf['sheets_uuid'].isnull()].drop(columns='sheets_uuid')
    #pp.pprint(joindf)
    return joindf
    
    
def insertNewData(mintdf, sheetsdf, row_num):
    rows_list = joinDFs(mintdf, sheetsdf).values.tolist()   
    vals = [[replace_nans(r) for r in row] for row in rows_list]
    SPREADSHEET.values_update('transactions!A{}'.format(row_num)
                              , params={'valueInputOption': 'RAW'}
                              , body={'values': vals}
                              )

    

def main():
    print("Creating mint api connection")
    mint = mintapi.Mint(**mintParams())
    parse_and_write_transactions(mint.get_transactions_csv())
    mintdf, sheetsdf = tempTransactions(), sheetsTransactions()
    #pp.pprint(mintdf)
    #pp.pprint(sheetsdf)
    insertNewData(mintdf, sheetsdf, len(sheetsdf) + 2)



if __name__ == "__main__":
    main()
