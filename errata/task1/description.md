After a good night's sleep, I looked back and realized I made a fatal mistake with regards to how `Receipts` and `ReceiptItems` are joined. I originally made a `Receipts.rewardsReceiptItemListID` column that stores the primary key of ReceiptItems. This only makes sense if there is at most one `ReceiptItems` per `Receipt`, which isn't true: each item bought on the receipt should be its own `ReceiptItems`. I've attached a new diagram that shows how this should be modelled. Instead of a `Receipts.rewardsReceiptItemListID` column, there should instead be a `ReceiptItems.receiptId` can join to `Receipts._id`. That way, if we want data for the items on a given single receipt, as well as data from the receipt metadata, we can do something like

```mysql
SELECT i.itemPrice, i.finalPrice, i.pointsEarned, r.userId
FROM ReceiptItems i
JOIN Receipts r
ON i.receiptId = r._id
WHERE i.receiptId = \<id\>
```


This will require me to rewrite my queries for question 5 and 6 as well.
