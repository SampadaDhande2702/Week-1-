Day 3 ETL pipeline

Extract Transform and Load
It is a process used in data engineering to move data from one place to another in a clean and organized way.

Extract
This means collecting data from different sources.

Transform
This means cleaning and changing the data so it becomes useful.

Load
This means putting the cleaned data into a final system (usually a Data Warehouse).

Why ETL
For predictiong something from data, raw data is inefficient so we need to extract -> transform -> load

Why ELT
Beacause when the big data is there
You are a company and you get:
10 lakh rows of data every hour 
From website, app, payment system, etc.

In ELT:
Just take raw data.
Quickly dump it into warehouse.
Clean it later using powerful system.


3 Tables 
1)Customers
2)Products
3)Orders

1)Data is generated 
2)Data is stored in pd.dataframes (Table with rows and columns)

3)pd.read_csv(We take that data in our program)

4)Print the dataset

5) I am checking whether data is good or not

6)Checking quality of data
  1)rows and columns
  2)Null values total count
  3)Duplicate analysis in percentage
  4)Unique value counts
  5)Datatype counts

7)Visualization of all null values and duplicates

8)How to handle null values filled with unknown,zero and city with newyork

9)How to handle duplicates

TRANSFORM


JOINS

Merging Datasets - Step by Step
Merged te rows and columns by joins

Concatenation - Combining Similar DataFrames
Sepration of dataframes-because you wanted to separate the orders based on time (quarter).
Then combinging it by using concat function


Pivoting & Unpivoting
The pivot table was created to summarize the dataset by counting how many orders occurred in each product category for every month, making the data easier to analyze.


Feature engg
Feature engineering means creating new useful columns from existing data so that analysis or machine learning becomes easier.

Business Rule Implementation
This function applies business rules to the dataset.
Business rules mean logic used by a company to make decisions automatically.

Example:
“VIP customers should get higher discounts.”

SECTION 4: Load & Pipeline Orchestration
4.1 Loading to CSV


Logging = writing program activities into a file.
2026-03-06 10:20:01 - ETL_Pipeline - INFO - Attempting to extract: customers.csv
2026-03-06 10:20:02 - ETL_Pipeline - INFO - Successfully extracted 500 rows
2026-03-06 10:20:03 - ETL_Pipeline - ERROR - File not found: orders.csv

What is Orchestration?

Orchestration = automatically controlling and running the steps of a data pipeline.
