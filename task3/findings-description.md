Below are the data quality concerns that I've found with the given JSON files. I've also included some things that I thought might be a concern but turned out weren't. All research was done with either Bash or Python run on the JSON files themselves -- I did not transform the data at this point. My code is inserted below and also uploaded in this directory. The other .md in this directory, findings-email.md, will have the results formatted and described for a product or business leader not familiar with my work.

# Concerns with Reciepts

## Missing data keys in the schema

While the schema provided gives us information about most of the keys in the data, the nested JSON object in rewardsReceiptItemList was undocumented. In order to find out what keys existed in this object, I ran the following
Python script:

```python
import json

data = []
with open('receipts.json') as receipts_data:
    for line in receipts_data:
        data.append(json.loads(line))
receiptsLoad = json.loads(json.dumps(data))  # python can't handle multiple objects at once normally. this is a quick workaround

ReceiptItemList = set()
for x in receiptsLoad:
    for key in x:
        if key == 'rewardsReceiptItemList':
            for itemList in x[key]:
                for key2 in itemList:
                    ReceiptItemList.add(key2)

print(ReceiptItemList)

#{'finalPrice', 'originalMetaBriteDescription', 'brandCode', 'itemPrice', 'needsFetchReviewReason', 'description', 'partnerItemId', 'barcode', 'targetPrice', 'originalReceiptItemText', 'needsFetchReview', 'competitiveProduct', 'preventTargetGapPoints', 'pointsPayerId', 'metabriteCampaignId', 'itemNumber', 'userFlaggedQuantity', 'userFlaggedNewItem', 'userFlaggedPrice', 'originalMetaBriteItemPrice', 'competitorRewardsGroup', 'deleted', 'userFlaggedDescription', 'userFlaggedBarcode', 'rewardsGroup', 'priceAfterCoupon', 'rewardsProductPartnerId', 'discountedItemPrice', 'originalMetaBriteQuantityPurchased', 'pointsEarned', 'pointsNotAwardedReason', 'quantityPurchased', 'originalMetaBriteBarcode', 'originalFinalPrice'}

```

As I described in task 1, there is no guarantee that ths is the full set of keys over all the data, but for the sake of this exercise I am operating under the assumption that it is. While I was able to document the names of the headers, I still do not know what some of them represent. For example, `deleted` or `pointsPayerId` is a little ambigious. I would need someone with domain knowledge to fill in those gaps for me.

## Duplicate data? barcode vs originalMetaBarcode
Within receipts[ReceiptItemList], there are two keys that seems similar at first glance: `barcode` and `originalMetaBriteBarcode`. Manually going through the JSON, it seemed like if there was an `originalMetaBriteBarcode`, then it was the same as `barcode`. I figured that, even if the two barcodes aren't the same for a given item, if there is a one to one relationship between barcodes and MetaBriteBarcodes, then we can consider MetaBriteBarcodes duplicate data and store is elsewhere. I wrote the following Python script to see if that was true:

```python
import json

data = []
with open('receipts.json') as receipts_data:
    for line in receipts_data:
        data.append(json.loads(line))
receiptsLoad = json.loads(json.dumps(data))  # python can't handle multiple objects at once normally. this is a quick workaround

# duplicate barcode data
barcode_dict = {}
for x in receiptsLoad:
    if 'rewardsReceiptItemList' in x:
        for y in x['rewardsReceiptItemList']:
            if 'barcode' in y:
                barcode = y['barcode']
                if barcode not in barcode_dict:
                    barcode_dict[barcode] = None
                if 'originalMetaBriteBarcode' in y:
                    MBbarcode = y['originalMetaBriteBarcode']
                    if (barcode_dict[barcode] is None or
                            barcode_dict[barcode] == [MBbarcode]):  # wrapping with a list is a quick and dirty way to
                        barcode_dict[barcode] = [MBbarcode]         # potentially append multiple values if needed
                    else:
                        barcode_dict[barcode].append(MBbarcode)
                        print(f'{barcode} has multiple MBbarcodes.')
for key in barcode_dict:
    print(key, barcode_dict[key])

# a truncated output:
# 4011 has multiple MBbarcodes.
# 4011 has multiple MBbarcodes.
# 4011 has multiple MBbarcodes.
# 4011 has multiple MBbarcodes.
# 4011 ['028400642255', '', '', '028400642255', '028400642255']
# 028400642255 None
# 1234 None
# 046000832517 None
# 013562300631 None
# 034100573065 ['034100573065']
# 075925306254 ['075925306254']
```
I found that the only barcode associated with multiple originalMetaBriteBarcodes is `4011`. If we can figure out what is so special about `4011`, then we can create a lookup table to store each `originalMetaBriteBarcode` and its associated barcode, and eliminate a column from `ReceiptItems`, as the relationship between the two keys is otherwise at most one-to-one.

### What is so special about 4011?
Once again, I took a look manually and found that a `barcode` of `4011` was often associated with a description of  `ITEM NOT FOUND`. It seems like `4011` is a placeholder barcode. I used the following Bash script to see if that is true.

```bash
grep -E '4011","description":.{20}' -o receipts.json

# searches for strings in receipts.json that matches the following regular expression pattern:
# the string '"4011", description":' followed by any 20 characters. We are returning just the matched text rather than the entire line that the matched text is part of.
```

Unfortunately here, my hypothesis was not true. Here's a snippet of some of the results:

```
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"BANANAS","discounte
4011","description":"BANANAS","discounte
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"ITEM NOT FOUND","fi
4011","description":"Yellow Bananas","di
4011","description":"Yellow Bananas","di
4011","description":"Yellow Bananas","di
4011","description":"Yellow Bananas","di
4011","description":"Yellow Bananas","di
4011","description":"ITEM NOT FOUND","fi
```
This barcode is also used for bananas and yellow bananas. Its still strange to me that the only descriptions in the dataset are 'Yellow Bananas', 'BANANAS', and 'ITEM NOT FOUND'. I would like to do some further research into what this barcode is meant to represent, as this data now seems pretty shoddy, but I unfortunately don't think the answers to my question is in the data itself. Instead, I would have to talk to a barcode expert to see if they know what is going on here. (Or I can Google '4011 barcode' and get the answer, but I still think that meeting up with an expert is the correct way to go for these kinds of things.)

## If Item Not Found, what do we do next?
Speaking of `ITEM NOT FOUND`, it sounds like this data point should essentially flag this row for manual review so that the item can eventually be found. 'Receipts[rewardsReceiptItemList][needsFetchReview]' looks like it acts as that flag. I would expect this to be true for any item that has a description of 'ITEM NOT FOUND'. Unfortunately, that is not the case:

```bash 
grep -E 'ITEM NOT FOUND".+needsFetchReview":true\}' receipts.json

# searches for strings that match the following pattern:
# the string 'ITEM NOT FOUND".' followed by any number of characters followed by the string 'needsFetchReview":true}'
```
returns no results. This seems like a gap to me, and I think that any time we have an "ITEM NOT FOUND' or something similar, we should be manually reviewing those items in hopes of reducing the overall number of 'ITEM NOT FOUND's that we see.

## The dates are good, but I'm glad I checked
I noticed that the dates are stored as integers and not as ISO dates. I guessed that they were Linux timestamps and was fortunately correct right off the bat. I figured it would be a good idea to confirm that none of the dates are particularly weird: nothing from too long ago or in the future. I wrote the following bash one-liner to confirm:

```bash
grep -E '"\$date":[0123456789]{13}' -o receipts.json | grep -E [0123456789]{10} -o | while read line; do date -d '@'$line; done > receiptsEpochTime'

# searches for strings that are just 13 digits, pulls the first 10 of those digits (as I don't care about the milliseconds), adds an '@' in front of the number for the sake of formatting, transforms them into human readable dates via the GNU program, date, and pipes them into a file named receiptsEpochTime.
```

With that `receiptsEpochTime`, I'm able to quickly `grep` for any year I want to search for, say 2020, with a `grep '2020' receiptsEpochTime`. I've confirmed that all dates are within 2017 and 2021, although there are very few 2017s compared to the rest.

# Concerns with Brands
## There are a lot of test brands
Looking manually at the JSON, we're immediately greeted with the word "test" everywhere on the screen, which seems wrong. We can find the total line count of the file with a `wc -l brands.json` and see that there are 1167 lines, and so, assuming one brand per line, that there are 1167 brands in the file. If we do a very naive search and line count of just the phrase 'test brand', using `grep 'test brand' brands.json | wc -l`, we get 428 results. That means that at least a third of our brands are test brands. While such data can be useful in testing and development situations, it shouldn't be entering production. Until we've investigated where this data is coming from, I would not load this data into a data warehouse.

# Concerns with Users
## Are they test users?
Since PII has been scrubbed from this file, and since test user records are usually identified by their name, we cannot from this data alone tell if there are test users in our file. However, it is something that should be looked into if at all possible, given our issues with Brands.

## There are non-consumers in the data
According to the Users data schema, role is a "constant value set to 'CONSUMER'". We can quickly `grep` to see if that is true:

```bash
grep -E 'role":"[^c]' -i users.json

#looks for strings of the following pattern:
# 'role":" followed by any character that is not 'c' or 'C'
```
The following truncated snippet shows that we have a number of fetch staff in the data as well:

```
{"_id":{"$oid":"59c124bae4b0299e55b0f330"},"active":true,"createdDate":{"$date":1505830074302},"lastLogin":{"$date":1612802578117},"role":"fetch-staff","state":"WI"}
{"_id":{"$oid":"59c124bae4b0299e55b0f330"},"active":true,"createdDate":{"$date":1505830074302},"lastLogin":{"$date":1612802578117},"role":"fetch-staff","state":"WI"}
{"_id":{"$oid":"59c124bae4b0299e55b0f330"},"active":true,"createdDate":{"$date":1505830074302},"lastLogin":{"$date":1612802578117},"role":"fetch-staff","state":"WI"}
{"_id":{"$oid":"59c124bae4b0299e55b0f330"},"active":true,"createdDate":{"$date":1505830074302},"lastLogin":{"$date":1612802578117},"role":"fetch-staff","state":"WI"}
```
The data description contradicts what is actually going on in the data, which means that either the schema description needs to be updated or the data is wrong. We would need to talk to business to determine which is the case, but it wouldn't be too hard of a fix either way. If the data is wrong, we would simply need to filter by role before loading this data into the warehouse. If the description is wrong, we need to document all possible values of `role`.


## The dates are still good, and I'm still glad I checked.
There are two date-related things that I can potentially see go wrong here. The first is the same as what we checked in Receipts: are there any weird dates in the file? The second is whether any 'lastLogin' are before the 'created-Date'. Both are easy enough to check for.

We can reuse my bash one-liner on this file and similarly grep for any weird years:

```bash
grep -E '"\$date":[0123456789]{13}' -o users.json | grep -E [0123456789]{10} -o | while read line; do date -d '@'$line; done > usersEpochTime
```

Nothing particluarly weird, which is good. I looked for dates 2013 or earlier, as that is when Fetch was founded, and of course for dates in the future.

I wrote the following Python script to check for `lastLogins` earlier than `created-Date`:

```python
data = []
with open('users.json') as users_data:
    for line in users_data:
        data.append(json.loads(line))
usersLoad = json.loads(json.dumps(data))  # python can't handle multiple objects at once normally. this is a quick workaround

for x in usersLoad:
    createdDate = 0
    lastLogin = 0
    for key in x:
        if key == 'createdDate':
            createdDate = x[key]
        if key == 'lastLogin':
            lastLogin = x[key]
    if lastlogin - createdDate < 0:
        print(x['_id'])
```

This gets the integers representing last login and created Date, and if a user's last login is smaller than created Date, then it prints the ID of that user. Nothing was printed out, which means we are in the clear.

