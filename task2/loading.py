# The below creates csvs that can be loaded into a database. In production, I would use either an ORM like sqlalchemy or a SQL connector like the mysql.connector library.

import json
import csv
from time import strftime, localtime


def load_data(filename):
    data = []
    with open(filename) as receipts_data:
        for line in receipts_data:
            data.append(json.loads(line))
    return json.loads(json.dumps(data))  # python can't handle multiple objects at once normally.
    # this is a quick workaround


def create_receipt_table(receiptLoad):
    with open('receipts.csv', "w") as file:
        filewriter = csv.writer(file, delimiter="\t")
        for x in receiptLoad:
            _id = x['_id']['$oid']
            epochTime = x['createDate']['$date']
            createDate = strftime('%Y-%m-%d %H:%M:%S', localtime(epochTime/1000))
            rewardsReceiptItemListID = _id  # deciding to use the same ID for both as a POC
            try:
                totalSpent = x['totalSpent']
            except KeyError:
                totalSpent = 0
            rewardsReceiptStatus = x['rewardsReceiptStatus']
            try:
                purchasedItemCount = x['purchasedItemCount']
            except KeyError:
                purchasedItemCount = None
            row = [_id, createDate, totalSpent, rewardsReceiptStatus, purchasedItemCount]
            
            filewriter.writerow(row)


def create_rec_items_table(receiptLoad):
    # for performance reasons, this could technically be done inside the above function. but that isn't
    # readable or maintainable
    with open('receipts_item.csv', "w") as file:
        filewriter = csv.writer(file, delimiter="\t")
        for x in receiptLoad:
            receiptId = x['_id']['$oid']
            if 'rewardsReceiptItemList' in x:
                for itr, receiptItems in enumerate(x['rewardsReceiptItemList']):
                    if 'barcode' in receiptItems:
                        barcode = receiptItems['barcode']
                        _id = str(receiptId) + str(itr+1)
                        row = [_id, barcode, receiptId]
                        filewriter.writerow(row)


def create_brands_table(brandsLoad):
    with open('brands.csv', "w") as file:
        filewriter = csv.writer(file, delimiter="\t")
        for x in brandsLoad:
            _id = x['_id']['$oid']
            barcode = x['barcode']
            name = x['name']

            row = [_id, barcode, name]
            filewriter.writerow(row)


RL = load_data('receipts.json')
create_receipt_table(RL)
create_rec_items_table(RL)

BL = load_data('brands.json')
create_brands_table(BL)
