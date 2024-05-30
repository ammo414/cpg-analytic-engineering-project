# The below creates rows that I can manually insert into a databse. I would *NEVER* do such a thing 
# with production data. The below loading functions are susceptible to SQL injections, requires me to manually 
# turn python "None"s into SQL "NULL"s, isn't guaranteed to format dates correctly, etc. But it does let me play with 
# the data enough to test my queries.

# In production, I would use either an ORM like sqlalchemy or a SQL connector like the mysql.connector library.

import json
from time import strftime, localtime


def load_data(filename):
    data = []
    with open(filename) as receipts_data:
        for line in receipts_data:
            data.append(json.loads(line))
    return json.loads(json.dumps(data))  # python can't handle multiple objects at once normally.
    # this is a quick workaround


def create_receipt_table(receiptLoad):
    for x in receiptLoad:
        _id = x['_id']['$oid']
        epochTime = x['createDate']['$date']
        createDate = strftime('%Y-%m-%d %H:%M:%S', localtime(epochTime/1000))
        rewardsReceiptItemListID = _id  # deciding to use the same ID for both as a POC
        try:
            totalSpent = x['totalSpent']
        except KeyError:
            totalSpent = None
        rewardsReceiptStatus = x['rewardsReceiptStatus']
        try:
            purchasedItemCount = x['purchasedItemCount']
        except KeyError:
            purchasedItemCount = None
        row = f'("{_id}","{createDate}","{rewardsReceiptItemListID}",{totalSpent},"{rewardsReceiptStatus}","{purchasedItemCount}"),'
        print(row)


def create_rec_items_table(receiptLoad):
    # for performance reasons, this could technically be done inside the above function. but that isn't
    # readable or maintainable
    for x in receiptLoad:
        _id = x['_id']['$oid']
        if 'rewardsReceiptItemList' in x:
            for receiptItems in x['rewardsReceiptItemList']:
                if 'barcode' in receiptItems:
                    barcode = receiptItems['barcode']
                else:
                    barcode = None

        row = f'("{_id}",{barcode}),'
        print(row)


def create_brands_table(brandsLoad):
    for x in brandsLoad:
        _id = x['_id']['$oid']
        barcode = x['barcode']
        name = x['name']

        row = f'("{_id}",{barcode},"{name}"),'
        print(row)


RL = load_data('receipts.json')
create_receipt_table(RL)
create_rec_items_table(RL)

BL = load_data('brands.json')
create_brands_table(BL)

