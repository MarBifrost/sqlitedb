import sqlite3
from faker import Faker
from datetime import datetime

# Initialize connection and Faker, creating database and cursor object
conn = sqlite3.connect('books_and_authors.sqlite3')
cursor = conn.cursor()
fake = Faker()

# create of authors' and books' tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        author_name TEXT NOT NULL,
        surname TEXT NOT NULL,
        birthdate DATE NOT NULL,
        birthplace TEXT NOT NULL,
        author_ID INTEGER NOT NULL
    )

""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        pages INTEGER NOT NULL,
        publishing_date DATE NOT NULL,
        author_ID INTEGER,
        FOREIGN KEY(author_ID) REFERENCES authors(author_ID)
    )

 """)
for i in range(500):
    author_name = fake.first_name()
    author_surname = fake.last_name()
    author_birthdate = fake.date_of_birth(minimum_age=25, maximum_age=100)
    author_birthplace = fake.city()
    author_ID = fake.random_int(min=0, max=500)

    cursor.execute("""
        INSERT INTO authors (author_name, surname, birthdate, birthplace, author_ID) VALUES (?, ?, ?, ?, ?)
    """, (author_name, author_surname, author_birthdate, author_birthplace, author_ID))

# Fetch author IDs for assigning to books
cursor.execute("SELECT author_ID FROM authors")
author_ids = [row[0] for row in cursor.fetchall()]
# define the time range for books publishing years data
start_date = datetime(1925, 1, 1).date()
end_date = datetime.today().date()
# insert 1000 fake authors into the table 'books'
for i in range(1000):
    book_title = fake.word()
    book_category = fake.word()
    book_pages = fake.random_int()
    book_publishing_date = fake.date_between(
        start_date=start_date, end_date=end_date)
    author_ID = fake.random_element(author_ids)

    cursor.execute("""
        insert into books (title, category, pages, publishing_date, author_ID)
        values (?, ?, ?, ?, ?)
    """, (book_title, book_category, book_pages, book_publishing_date, author_ID))

#Query to find the book with the most pages
cursor.execute("""
    select * from books order by pages desc limit 1;
""")

pages = cursor.fetchone()
most_pages = f"Book ID: {pages[0]}\nTitle: {pages[1]}\nCategory: {pages[2]}\nPages: {pages[3]}\nPublish Date: {pages[4]}\nAuthor ID: {pages[5]}\n"
print(f"The book with the most pages: \n{most_pages}")

# query to calculate the average number of pages, also it's rounded to the nearest integer
cursor.execute("""
    select round(avg(pages)) as avg_pages from books;
""")

avg_pages = cursor.fetchone()
print(f"The average number of pages: \n{int(avg_pages[0])}\n")

# query to find the youngest author
cursor.execute("""
    select author_name, surname, birthdate from authors order by birthdate desc limit 1;
""")
youth = cursor.fetchone()
print(f"The youngest authors: \n{youth[0]} {youth[1]} born in {youth[2]}\n")

# query to find the authors without any books
cursor.execute("""
    select a.author_name, a.surname from authors a left join books b on a.author_ID = b.author_ID where b.author_ID is null;
""")

authors_without_books = cursor.fetchall()
no_books = ''.join(
    [f"{no_book[0]} {no_book[1]}\n" for no_book in authors_without_books])
print(f"The authors without any books: \n{no_books}")


# query to find authors with more than 3 books
cursor.execute("""
    SELECT a.author_ID, a.author_name, a.surname, COUNT(b.ID) as book_count
    FROM authors a
    INNER JOIN books b ON a.author_ID = b.author_ID
    GROUP BY a.author_ID
    HAVING COUNT(b.ID) > 3
    LIMIT 5;
""")

authors_with_3_books = cursor.fetchall()
authors_with_books = ''.join(
    [f"{author[1]} {author[2]} \n" for author in authors_with_3_books])
print(f"Authors with more than 3 books:\n{authors_with_books}")

#Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
