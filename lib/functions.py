import json
import csv
import re
import math

def openFile(path, file):
    type = file.split('.')[-1]
    if type == 'json':
        with open("{}/{}".format(path, file)) as f:
            v = json.load(f)
    elif type == 'sql':
        with open("{}/{}".format(path, file)) as f:
            v = f.read()
    elif type == 'csv':
        v = pd.read_csv('{}/{}'.format(path, file))
    elif type == 'pw':
        with open("{}/{}".format(path, file)) as f:
            v = f.read()
    return v


def split_transactions(transactrow):
    return [t.replace('"', '') for t in re.split(r',(?=")', transactrow)] 

def replace_bad_chars(t):
    return t.replace('nan', '')

def parse_and_write_transactions(t, write_path='.'):
    '''
    t: result of mintapi.Mint().get_transactions_csv()
    write_path: location you want to store the temporary transactions csv
    
    '''
    #transactions = replace_bad_chars(str(t, 'utf-8')).split("\n")
    transactions = str(t, 'utf-8').split("\n")
    with open('{}/.temp_transactions.csv'.format(write_path), 'w') as f:
        writer = csv.writer(f)
        for row in transactions:
            writer.writerow(split_transactions(row))


def replace_nans(t):
    try:
        if math.isnan(t):
            return ''
        else:
            return t
    except:
        return t

def create_sudo_id_field(cols):
    val = re.sub(r'\W+', '', (''.join([str(i) for i in cols])).lower())
    return val



def update_col_format(spreadsheet, sheet):
    requests = [{
        "repeatCell": {
            "range": {
                "startColumnIndex": 0,
                "endColumnIndex": 1,
                "sheetId": sheet._properties['sheetId']
            },
        "cell": {
             "userEnteredFormat": {
                "numberFormat": {
                "type": "DATE",
                "pattern": "mm/dd/yyy"
                    }
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    }]
    body = {
        'requests': requests
    }
    res = spreadsheet.batch_update(body)



