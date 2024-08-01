
## Fetch Rewards Coding Exercise - Analytics Engineer
In this exercise I:

Demonstrated how I reason about data and how I communicate my understanding of a specific data set to others.
What are the requirements?

* Review unstructured JSON data and diagram a new structured relational data model
* Generate a query that answers a predetermined business question
* Generate a query to capture data quality issues against the new structured relational data model
* Write a short email or Slack message to the business stakeholder

### First: Review Existing Unstructured Data and Diagram a New Structured Relational Data Model


Review the 3 sample data files provided below. Develop a simplified, structured, relational diagram to represent how I would model the data in a data warehouse. The diagram should show each table’s fields and the joinable keys. 

### Second: Write queries that directly answer predetermined questions from a business stakeholder

Write SQL queries against my new structured relational data model that answer the following bullet points below.

* What are the top 5 brands by receipts scanned for most recent month?
* How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?
* When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
* When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?
* Which brand has the most spend among users who were created within the past 6 months?
* Which brand has the most transactions among users who were created within the past 6 months?

### Third: Evaluate Data Quality Issues in the Data Provided

Identify as many data quality issues as I can.

### Fourth: Communicate with Stakeholders

Construct an email or slack message that is understandable to a product or business leader who isn’t familiar with my day to day work. This part of the exercise should show off how I communicate and reason about data with others.

* What questions do I have about the data?
* How did I discover the data quality issues?
* What do I need to know to resolve the data quality issues?
* What other information would I need to optimize the data assets I am trying to create?
* What performance and scaling concerns do I anticipate in production and how do I plan to address them?

The Data
Receipts Data Schema

    _id: uuid for this receipt
    bonusPointsEarned: Number of bonus points that were awarded upon receipt completion
    bonusPointsEarnedReason: event that triggered bonus points
    createDate: The date that the event was created
    dateScanned: Date that the user scanned their receipt
    finishedDate: Date that the receipt finished processing
    modifyDate: The date the event was modified
    pointsAwardedDate: The date we awarded points for the transaction
    pointsEarned: The number of points earned for the receipt
    purchaseDate: the date of the purchase
    purchasedItemCount: Count of number of items on the receipt
    rewardsReceiptItemList: The items that were purchased on the receipt
    rewardsReceiptStatus: status of the receipt through receipt validation and processing
    totalSpent: The total amount on the receipt
    userId: string id back to the User collection for the user who scanned the receipt

Users Data Schema

    _id: user Id
    state: state abbreviation
    createdDate: when the user created their account
    lastLogin: last time the user was recorded logging in to the app
    role: constant value set to 'CONSUMER'
    active: indicates if the user is active; only Fetch will de-activate an account with this flag

Brand Data Schema

    _id: brand uuid
    barcode: the barcode on the item
    brandCode: String that corresponds with the brand column in a partner product file
    category: The category name for which the brand sells products in
    categoryCode: The category code that references a BrandCategory
    cpg: reference to CPG collection
    topBrand: Boolean indicator for whether the brand should be featured as a 'top brand'
    name: Brand name

