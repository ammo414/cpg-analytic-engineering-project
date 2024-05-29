# contains all the bash one-liners used to research data quality issues. Since these are one-liners, they were intended to be run in a terminal, rather than as a proper script.

# barcode 4011 and its related descriptions:
# searches for strings in receipts.json that matches the following regular expression pattern:
# the string '"4011", description":' followed by any 20 characters. We are returning just the matched text rather than the entire line that the matched text is part of.

grep -E '4011","description":.{20}' -o receipts.json


# ITEM NOT FOUND and its lack of needing review:
# searches for strings that match the following pattern:
# the string 'ITEM NOT FOUND".' followed by any number of characters followed by the string 'needsFetchReview":true}'

grep -E 'ITEM NOT FOUND".+needsFetchReview":true\}' receipts.json


# converting linux timestamps into human readable dates for further grepping
# searches for strings that are just 13 digits, pulls the first 10 of those digits (as I don't care about the milliseconds), adds an '@' in front of the number for the sake of formatting, 
# transforms them into human readable dates via the GNU program, date, and pipes them into a file named receiptsEpochTime.

grep -E '"\$date":[0123456789]{13}' -o receipts.json | grep -E [0123456789]{10} -o | while read line; do date -d '@'$line; done > receiptsEpochTime'

grep '2020' receiptsEpochTime


# finding the number of lines in brands.json that has the phrase 'test brand'

grep 'test brand' brands.json | wc -l


