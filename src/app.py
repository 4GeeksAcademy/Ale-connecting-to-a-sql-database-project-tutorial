import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Connect DB
connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
engine = create_engine(connection_string).execution_options(autocommit=True)
engine.connect()

# Create tables
engine.execute("""
CREATE TABLE IF NOT EXISTS publishers(
    publisher_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY(publisher_id)
);

CREATE TABLE IF NOT EXISTS authors(
    author_id INT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(50) NULL,
    last_name VARCHAR(100) NULL,
    PRIMARY KEY(author_id)
);

CREATE TABLE IF NOT EXISTS books(
    book_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    total_pages INT NULL,
    rating DECIMAL(4, 2) NULL,
    isbn VARCHAR(13) NULL,
    published_date DATE,
    publisher_id INT NULL,
    PRIMARY KEY(book_id),
    CONSTRAINT fk_publisher FOREIGN KEY(publisher_id) REFERENCES publishers(publisher_id)
);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY(book_id, author_id),
    CONSTRAINT fk_book FOREIGN KEY(book_id) REFERENCES books(book_id) ON DELETE CASCADE,
    CONSTRAINT fk_author FOREIGN KEY(author_id) REFERENCES authors(author_id) ON DELETE CASCADE
);
""")

# Insert data
engine.execute("""
INSERT INTO publishers(publisher_id, name) VALUES (1, 'Allen & Unwin')
ON CONFLICT (publisher_id) DO NOTHING;

INSERT INTO authors (author_id, first_name, middle_name, last_name) VALUES (1, 'John', 'Ronald Reuel', 'Tolkien')
ON CONFLICT (author_id) DO NOTHING;

INSERT INTO books (book_id, title, total_pages, rating, isbn, published_date, publisher_id) VALUES (1, 'The Lord of the Rings', 1216, 4.5, '9780261102385', '1954-07-29', 1)
ON CONFLICT (book_id) DO NOTHING;

INSERT INTO book_authors (book_id, author_id) VALUES (1, 1)
ON CONFLICT (book_id, author_id) DO NOTHING;
""")

# Print table
result_dataFrame = pd.read_sql("SELECT * FROM publishers;", con=engine)
print(result_dataFrame)