# Books and Authors Database with python/sqlite

## Description
This project creates and manages sqlite database

## Requirements
- python 3.x<br>
- sqlite3
- Faker and datatime libraries


## installation
clone the repository or download the script:<br>
**git clone https://github.com/MarBifrost/my_sqlitedb**<br>
**cd to the repository folder**<br>
**install required dependencies:**<br>
pip install faker<br>
**run the script**<br>
python/python3 sqlitedb.py


## Usage
Create sqlite Database and tables which are stored as 'Books_and_authors.sqlite3' in the script.
Generate and inserts fake data with faker
Run queries for following data:
-Find the book with the most pages
-Calculate the average number of pages in the table 'books'
-Find the youngest author in the Database
-Detect if there are any authors without books
-As least 5 authors who have written more than three books

## Known Issues
- Query for authors without books might not return the expected results
