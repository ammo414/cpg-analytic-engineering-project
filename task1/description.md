In order to model the provided data, I decided to make `Users` and `Brand` into their own tables. There's nothing too interesting going on here, as `_id` is used as the primary key for both tabes and `Users._id` joins to `Receipts.userId` as expected. However, at first glance it doesn't look like `Brands` can join to any other table. I'll explain how I handled that after I explain how I decided to model `Receipts`.

I broke up `Receipts` into two tables. One of them, `Receipts`, stores what I consider the metadata of the receipts, while `ReceiptItems` stores the data of the items purchased themselves. In practice, this meant that all the keys in `rewardsReceiptItemList` was flattened and modeled as `ReceiptItems` while everything else was kept in `Receipts`. Importantly, this means that a new `ReceiptItems` column will have to be created to store the primary key of `Receipts` so that a `ReceiptItem` can be joined back up to `Receipts`. I chose to do this because, with the `Receipts.totalSpent` and `Receipts.purchasedItemCount` columns, I realized that a good number of business questions can be answered without referencing the line-level data on the receipt. This meant that breaking up the table can result in more performant queries and a less wide table overall. This way, if we want data for the items on a given single receipt, as well as data from the receipt metadata, we can do something like

```mysql
SELECT i.itemPrice, i.finalPrice, i.pointsEarned, r.userId
FROM ReceiptItems i
JOIN Receipts r
ON i.receiptId = r._id
WHERE i.receiptId = \<id\>
```

I wrote a Python script to find all the undocumented keys within `ReceiptItemList`, which I describe further in task 3 - data quality issues. There's no guarantee that this sample of data has all the keys, but for the sake of this exercise I modeled my database under the assumption that this sample does contain all the keys. One of the keys that does show up consistently is `barcode`, which is fortunately also a key in `Brands`, and can likely be used as a secondary key in `Brands`. This means that we can join `Brands.barcode` on `ReceiptItems.barcode`, and then `ReceiptItems._id` on `Receipt.rewardsReceiptItemList` as needed.

One final thing to note is that I typed the date columns (`createDate`, `dateScanned`, etc.) as datetimes even though they are stored as Unix timestamps, that is, integers, in the JSON data. I expect this data to be transformed to a human readable and SQL friendly format during the transformation process to make things easier for folks consuming the data downstream of us. Similarly, I typed the price columns as floats even though they are currently strings. I am not sure this is correct, as I only have a basic understanding of floating point arithmetic and the issues involved with loading and transforning decimal data from one format to another. I do believe that storing prices as floats will allow for better mathematical manipulation downstream, though.



This will require me to rewrite my queries for question 5 and 6 as well.
