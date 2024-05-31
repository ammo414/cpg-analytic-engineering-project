5) Which brand has the most spend among users who were created within the past 6 months?
6) Which brand has the most transactions among users who were created within the past 6 months?

The following query answers both of the above.

```mysql
SELECT b.name
  , sum(i.itemPrice)
  , count(i.barcode)
FROM Brand b
JOIN ReceiptItems i
  on b.barcode = i.barcode
JOIN Receipts r
  on i.receiptId =  r._id
JOIN Users u
  on r.userId = i._id
WHERE i.createdDate >= CURDATE() - INTERVAL (DAYOFMONTH(CURDATE() -1) DAY - INTERVAL 6 MONTH
group by b._id
```

I had to modify a join statement to take into account how the tables should've actually been modelled. 
