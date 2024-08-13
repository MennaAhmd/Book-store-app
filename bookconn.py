import sqlite3

# Define the database name
DATABASE_NAME = 'dbfinl.db'

def setup_database():
    """Create the tables if they don't exist and populate with sample data."""
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    
    try:
        # Drop existing tables to reset AUTOINCREMENT
        c.execute("DROP TABLE IF EXISTS book_images")
        c.execute("DROP TABLE IF EXISTS book_prices")
        c.execute("DROP TABLE IF EXISTS books")
        
        # Create books table
        c.execute('''
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL UNIQUE,
            author TEXT,
            year INTEGER,
            genre TEXT,
            pages INTEGER
        )''')
        
        # Create book_images table
        c.execute('''
        CREATE TABLE book_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            image_path TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )''')
        
        # Create book_prices table
        c.execute('''
        CREATE TABLE book_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            price REAL,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )''')
        
        # Insert sample data into books table
        books = [
            ('Machine Learning: 4 Books in 1', 'Samuel Hack', 2020, 'Computer Science', 694),
            ('Cyber Security', 'Brian Walker', 2015, 'Computer Science', 320),
            ('ثاني أثنين', 'أدهم شرقاوي', 2020, 'دينى', 202),
            ('إيكادولي', 'حنان لاشين', 2017, 'روايات خياليه', 316),
            ('Rich Dad Poor Dad','Robert T. Kiyosaki',1997,'personal development',336),
            ('Atomic Habits','James Clear',2018,'Personal Development',320),
            ('Lonely Traveller','Sereno Sky',2014,'Travelogue',192),
            ('وهج البنفسج','اسامه المسلم',2017,'رعب',304),
('أماريتا','عمرو عبد الحميد',2016,'رويات خياليه',324),
('NLP: The Essential Guide to\n Neuro-Linguistic Programming',' Matheu Neil-Grass \nand Tom Hawkings',2009,'Personal Development',504),
('الماجريات ','إبراهيم السكران',2015,'ديني',343),
('Ghost in the Wires','Kevin Mitnick',2011,'Hacking',432),
('Theory of Applied Robotics','Reza N. Jazar',2022,'Robotics',883),
('Serious Python','Julien Danjou', 2018,'Programming',240),
('Data Science for \nBeginners: 2 Books in 1','Russel R. Russo',2020,'Data Science',378)
        ]
        
        # Insert books and store ids
        for book in books:
            c.execute('''
            INSERT INTO books (title, author, year, genre, pages) 
            VALUES (?, ?, ?, ?, ?)''', book)
        
        # Fetch book IDs
        c.execute("SELECT id FROM books ORDER BY id")
        book_ids = c.fetchall()
        
        # Insert sample data into book_images table
        book_images = [
            (book_ids[0][0], 'D:/Desktop/Book store project/img/ML.png'),
            (book_ids[1][0], 'D:/Desktop/Book store project/img/cyber.png'),
            (book_ids[2][0], 'D:/Desktop/Book store project/img/ثاني اثنين.png'),
            (book_ids[3][0], 'D:/Desktop/Book store project/img/ايكادولي.png'),
            (book_ids[4][0], 'D:/Desktop/Book store project/img/richdad.png'),
            (book_ids[5][0], 'D:/Desktop/Book store project/img/atomicH.png'),
            (book_ids[6][0], 'D:/Desktop/Book store project/img/lonley.png'),
            (book_ids[7][0], 'D:/Desktop/Book store project/img/وهج البنفسج.png'),
            (book_ids[8][0], 'D:/Desktop/Book store project/img/اماريتا.png'),
            (book_ids[9][0], 'D:/Desktop/Book store project/img/nlp.png'),
            (book_ids[10][0], 'D:/Desktop/Book store project/img/الماجريات.png'),
            (book_ids[11][0], 'D:/Desktop/Book store project/img/gostinwires.png'),
            (book_ids[12][0], 'D:/Desktop/Book store project/img/theory.png'),
            (book_ids[13][0], 'D:/Desktop/Book store project/img/python.png'),
            (book_ids[14][0], 'D:/Desktop/Book store project/img/datascience.png')
            
            
        ]
        
        c.executemany('''
        INSERT INTO book_images (book_id, image_path) VALUES (?, ?)''', book_images)
        
        # Insert sample data into book_prices table
        book_prices = [
            (book_ids[0][0], 450),
            (book_ids[1][0], 500),
            (book_ids[2][0], 360),
            (book_ids[3][0], 200),
            (book_ids[4][0], 400),
            (book_ids[5][0], 350),
            (book_ids[6][0], 250),
            (book_ids[7][0], 340),
            (book_ids[8][0], 260),
            (book_ids[9][0], 600),
            (book_ids[10][0],185),
            (book_ids[11][0], 300),
            (book_ids[12][0], 250),
            (book_ids[13][0], 340),
            (book_ids[14][0], 400)
            
        ]
        
        c.executemany('''
        INSERT INTO book_prices (book_id, price) VALUES (?, ?)''', book_prices)
        
        con.commit()
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        con.close()

setup_database()
