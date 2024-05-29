## contains all of the python scripts used to find data quality issues, better formatted than in findings-description.md

import json

# load receipts data
def load_data(filename):
    data = []
    with open(filename) as receipts_data:
        for line in receipts_data:
            data.append(json.loads(line))
    return json.loads(json.dumps(data))  # python can't handle multiple objects at once normally.
    # this is a quick workaround


# check for duplicate barcode data
def duplicate_barcode_check(receiptsLoad):
    barcode_dict = {}
    for x in receiptsLoad:
        if 'rewardsReceiptItemList' in x:
            for receiptItems in x['rewardsReceiptItemList']:
                if 'barcode' in receiptItems:
                    barcode = receiptItems['barcode']
                    if barcode not in barcode_dict:
                        barcode_dict[barcode] = None
                    if 'originalMetaBriteBarcode' in receiptItems:
                        MBbarcode = receiptItems['originalMetaBriteBarcode']
                        if (barcode_dict[barcode] is None or
                                barcode_dict[barcode] == [
                                    MBbarcode]):  # wrapping with a list is a quick and dirty way to
                            barcode_dict[barcode] = [MBbarcode]  # potentially append multiple values if needed
                        else:
                            barcode_dict[barcode].append(MBbarcode)
                            print(f'{barcode} has multiple MBbarcodes.')
    for key in barcode_dict:
        print(key, barcode_dict[key])


# ensure headers are correctly formatted and values are correctly typed
def header_formatting(receiptsLoad):
    receipts_headers = {'_id': str,
                        'bonusPointsEarned': int,
                        'bonusPointsEarnedReason': str,
                        'createDate': int,
                        'dateScanned': int,
                        'finishedDate': int,
                        'modifyDate': int,
                        'pointsAwardedDate': int,
                        'pointsEarned': int,
                        'purchaseDate': int,
                        'purchasedItemCount': int,
                        'rewardsReceiptItemList': list,
                        'rewardsReceiptStatus': str,
                        'totalSpent': float,
                        'userId': str}

    errorString = 'type error with '

    for x in receiptsLoad:
        for key in x:
            if key not in receipts_headers:
                print('unexpected header')
            if key == '_id':
                if type(x[key]['$oid']) is not str:
                    print(errorString + key)
            elif 'DATE' in key.upper():
                if type(x[key]['$date']) is not int:
                    print(errorString + key)
            elif key == 'totalSpent' or key == 'pointsEarned':
                try:
                    i = float(x[key])  # today I learned why decimals are stored as strings in JSON!
                except ValueError:
                    print(errorString + key)
            elif type(x[key]) is not receipts_headers[key]:
                print(errorString + key)


def find_all_missing_receipt_keys(receiptsLoad):
    ReceiptItemList = set()
    for x in receiptsLoad:
        for key in x:
            if key == 'rewardsReceiptItemList':
                for y in x[key]:
                    for key2 in y:
                        ReceiptItemList.add(key2)

    print(ReceiptItemList)
    return ReceiptItemList

def login_too_early_check(usersLoad):
    for x in usersLoad:
        createdDate = None
        lastLogin = None
        for key in x:
            if key == 'createdDate':
                createdDate = x[key]['$date']
            if key == 'lastLogin':
                lastLogin = x[key]['$date']
        if createdDate is not None and lastLogin is not None:
            if lastLogin - createdDate < 0:
                print(x['_id'])


if __name__ == '__main__':
    RL = load_data('receipts.json')
    duplicate_barcode_check(RL)
    header_formatting(RL)
    find_all_missing_receipt_keys(RL)

    UL = load_data('users.json')
    login_too_early_check(UL)
