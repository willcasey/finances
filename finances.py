import mintapi
import csv
import re

from lib.functions import *


#GLOBAL FUNCTIONS
LIB_PATH = "./lib/"
##


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

def main():
    mint = mintapi.Mint(**mintParams())
    parse_and_write_transactions(mint.get_transactions_csv())



if __name__ == "__main__":
    main()
