# question 1
SELECT b.name, count(b._id) as count_last_month
FROM Brand b
JOIN ReceiptItems i
  ON b.barcode = i.barcode
JOIN Receipts r
  ON i._id = r.rewardsReceiptItemListID
WHERE YEAR(r.createDate) = YEAR(CURDATE() - INTERVAL 1 MONTH)
  AND MONTH(r.createDate) = MONTH(CURDATE() - INTERVAL 1 MONTH)  
GROUP BY b.name
ORDER BY count_last_month DESC 
LIMIT 5

# question 2
SELECT b.name, count(b._id) as count_month_before_last
FROM Brand b
JOIN ReceiptItems i
  ON b.barcode = i.barcode
JOIN Receipts r
  ON i._id = r.rewardsReceiptItemListID
WHERE YEAR(r.createDate) = YEAR(CURDATE() - INTERVAL 2 MONTH)
  AND MONTH(r.createDate) = MONTH(CURDATE() - INTERVAL 2 MONTH)  
GROUP BY b.name
ORDER BY count_month_before_last DESC 
LIMIT 5

# questions 3 and 4
SELECT rewardsReceiptStatus
  , round(avg(totalSpent),2) AS averageSpent
  , sum(purchasedItemCount) AS totalPurchased
FROM Receipts
WHERE rewardsReceiptStatus = "REJECTED" 
  OR rewardsReceiptStatus = "ACCEPTED"
group by rewardsReceiptStatus

# worth pointing out that 'accepted' is not a value present in the data. Did you mean 'finished'?

# questions 5 and 6
SELECT b.name
  , sum(i.itemPrice)
  , count(i.barcode)
FROM Brand b
JOIN ReceiptItems i
  on b.barcode = i.barcode
JOIN Receipts r
  on i._id =  r.rewardsReceiptItemListID
JOIN Users u
  on r.userId = i._id
WHERE i.createdDate >= CURDATE() - INTERVAL (DAYOFMONTH(CURDATE() -1) DAY - INTERVAL 6 MONTH
group by b._id
