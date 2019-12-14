import json
import csv
import re

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


def split_transactions(t):
    return re.split(r',(?=")', t)



def parse_and_write_transactions(t, write_path='.'):
    '''
    t: result of mintapi.Mint().get_transactions_csv()
    write_path: location you want to store the temporary transactions csv
    
    '''
    transactions = str(t, 'utf-8').split("\n")
    with open('{}/.temp_transactions.csv'.format(write_path), 'w') as f:
        writer = csv.writer(f)
        for row in transactions:
            writer.writerow(split_transactions(row))
