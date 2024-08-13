import sqlite3

DATABASE_NAME = 'dbfinl.db'

def setup_database():
    """Create the tables if they don't exist."""
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    try:
        # Create users table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT NOT NULL UNIQUE,
                      password TEXT NOT NULL)''')

        # Create userinfo table with a foreign key to users table
        c.execute('''CREATE TABLE IF NOT EXISTS userinfo (
                      user_id INTEGER NOT NULL,
                      full_name TEXT,
                      phone TEXT,
                      email TEXT UNIQUE,
                      city TEXT,
                      location TEXT,
                      building_number TEXT,
                      floor_number TEXT,
                      FOREIGN KEY(user_id) REFERENCES users(id))''')

        # Create books table
        c.execute('''CREATE TABLE IF NOT EXISTS books (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL UNIQUE,
                      author TEXT,
                      year INTEGER,
                      genre TEXT,
                      pages INTEGER,
                      price REAL)''')

        # Create cart table
        c.execute('''CREATE TABLE IF NOT EXISTS cart (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      book_id INTEGER,
                      quantity INTEGER,
                      FOREIGN KEY(user_id) REFERENCES users(id),
                      FOREIGN KEY(book_id) REFERENCES books(id))''')

        # Create orders table
        c.execute('''CREATE TABLE IF NOT EXISTS orders (
                      order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      total_price REAL,
                      FOREIGN KEY(user_id) REFERENCES users(id))''')

        con.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def user_exists(username):
    """Check if a username already exists in the database."""
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    try:
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        return result is not None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        con.close()

def register_user(full_name, username, password):
    """Register a new user in the database."""
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    try:
        # Insert user into users table
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        user_id = c.lastrowid  # Get the user_id of the newly inserted user
        
        # Insert additional info into userinfo table
        c.execute("INSERT INTO userinfo (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
        
        con.commit()
        print("User registered successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()

def login_user(username, password):
    """Login a user by checking credentials."""
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    global logged_in_user_id  # Declare the global variable to store the logged-in user ID
    try:
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        result = c.fetchone()

        if result:
            user_id, db_password = result
            print(f"Stored password: {db_password}")  # للطباعة للتحقق

            if db_password == password:
                logged_in_user_id = user_id  # Store the user ID globally on successful login
                return user_id  # Return user_id on successful login
            else:
                print("Password does not match.")
        else:
            print("Username not found.")
        
        return None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        con.close()

def get_logged_in_user_id():
    """Get the logged-in user ID."""
    return logged_in_user_id

# Initialize the database
setup_database()
