Day 4
NumPy
Works with c and memory efficient
50 to 100 percent faster
python 28 byte each object
Numpy packs object tightly 8 byte each
used when we are training neural network
Only holds one datatype at a time


1)np.array()

2)np.arange()

3)np.zeros()

4).size

5).shape

6)SLicing

7)Numerial operations on array

8)Matrix multiplication
a.dot(b)

9)Loaded population dataset
10)argmax

11)mean

12)standard deviation

13)Broadcasting
NumPy automatically adjusts array sizes so mathematical operations can happen easily.


Broadcasting two arrays together follows these rules:

If the arrays do not have the same rank, prepend the shape of the lower rank array with 1s until both shapes have the same length.
The two arrays are said to be compatible in a dimension if they have the same size in the dimension, or if one of the arrays has size 1 in that dimension.
The arrays can be broadcast together if they are compatible in all dimensions.
After broadcasting, each array behaves as if it had shape equal to the elementwise maximum of shapes of the two input arrays.
In any dimension where one array had size 1 and the other array had size greater than 1, the first array behaves as if it were copied along that dimension


If arrays don’t have the same rank, add 1 at the beginning
Rank = number of dimensions
Example:

A shape = (2,3)
B shape = (3)

NumPy converts B to:
(1,3)
It automatically adds 1 in front so both shapes have the same length.


Pandas


What is pandas?
Pandas is a Python library used to work with data easily.
It helps you store, organize, clean, and analyze data in a simple way.

Think of pandas like an Excel sheet inside Python.

1)To read data easily
Pandas can read data from files like CSV, Excel, SQL databases, JSON, etc.

2)To organize data in tables
It stores data in a table format called DataFrame (rows and columns like Excel).

3)To clean data
You can remove duplicates, missing values, or wrong data.

4)To analyze data quickly
You can calculate sum, average, counts, group data, etc.

5)To filter and select data
Example: find orders above ₹1000 or customers from a specific city.

6)To prepare data for machine learning
Before training ML models, data usually needs cleaning and transformation. Pandas helps with that.

What is series in pandas?
A Series is a one-dimensional object that can hold any data type such as integers

What is a DataFrame in pandas?
A DataFrame is a table of data with rows and columns.


Indexing and Selecting Data in pandas means choosing specific rows or columns from a dataset.
In simple words:
It is the process of picking the data you want from a table.



Reading Data in CSV ,TABLE and TEXT


Statistical Analysis
sum
mean
median

What is Pivoting in pandas?
Pivoting means rearranging or reshaping data to see it in a better table format.

How to load the graph immediately

