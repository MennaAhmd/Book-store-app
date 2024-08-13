import tkinter as tk
from tkinter import Canvas, Frame
from PIL import Image, ImageTk
import sqlite3
import os
import dbfinl

DATABASE_NAME = 'dbfinl.db'
user_id = 2# Replace with actual user_id when integrating with login system

# Function to create a rounded rectangle
def create_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    canvas.create_oval(x1, y1, x1 + r * 2, y1 + r * 2, **kwargs)  # Top-left corner
    canvas.create_oval(x2 - r * 2, y1, x2, y1 + r * 2, **kwargs)  # Top-right corner
    canvas.create_oval(x1, y2 - r * 2, x1 + r * 2, y2, **kwargs)  # Bottom-left corner
    canvas.create_oval(x2 - r * 2, y2 - r * 2, x2, y2, **kwargs)  # Bottom-right corner
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)  # Middle horizontal
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)  # Middle vertical

# قائمة لحفظ الكتب المضافة إلى السلة
cart = []

# تحديث عرض سلة المشتريات
def update_cart_database(book_id, quantity):
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    try:
        if quantity > 0:
            c.execute('''
            UPDATE cart
            SET quantity = ?
            WHERE user_id = ? AND book_id = ?''', (quantity, user_id, book_id))
        else:
            c.execute('''
            DELETE FROM cart
            WHERE user_id = ? AND book_id = ?''', (user_id, book_id))
        con.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()


# إضافة كتاب إلى سلة المشتريات
def add_to_cart(book_id, quantity, user_id):
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    try:
        # Get the book details
        c.execute("SELECT title FROM books WHERE id = ?", (book_id,))
        book_title = c.fetchone()
        
        if book_title is None:
            print(f"Book ID {book_id} not found in the database.")
            return
        
        book_title = book_title[0]
        
        # Update the cart
        cart.append({"id": book_id, "title": book_title, "quantity": quantity})
        
        # Update the cart display
        update_cart_display()
        
        # Insert into the database
        c.execute('''
        INSERT INTO cart (user_id, book_id, quantity)
        VALUES (?, ?, ?)''', (user_id, book_id, quantity))
        
        con.commit()
        print(f"Added book ID {book_id} to cart with quantity {quantity}.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()
def update_cart_display():
    for widget in cart_frame.winfo_children():
        widget.destroy()
    
    for item in cart:
        cart_label = tk.Label(cart_frame, text=f"{item['title']} - Quantity: {item['quantity']}", font=('Arial', 12), bg='#B5CFB7')
        cart_label.pack(anchor='w')

def check_cart_table():
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    c.execute("SELECT * FROM cart")
    rows = c.fetchall()
    for row in rows:
        print(row)
    con.close()

# Call this function to check the content of the cart table
check_cart_table()


# Increase the quantity of books in the cart
def increase_quantity(book_id):
    global cart
    for item in cart:
        if item['id'] == book_id:
            item['quantity'] += 1
            update_cart_display()  # Update the TreeView display
            update_cart_database(book_id, item['quantity'])  # Update the database
            break


# Decrease the quantity of books in the cart
def decrease_quantity(book_id):
    global cart
    for item in cart:
        if item['id'] == book_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            else:
                cart.remove(item)
            update_cart_display()  # Update the TreeView display
            update_cart_database(book_id, item['quantity'])  # Update the database
            break

# الذهاب إلى صفحة الدفع
def go_to_checkout():
    if len(cart) == 0:
        tk.messagebox.showinfo("Cart is Empty", "Your cart is empty. Please add books before proceeding to checkout.")
        return

    root.destroy()
    import appi
    appi.show_frame()


# Show book details
def show_book_details(book_id):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT title, author, year, genre, pages FROM books WHERE id = ?", (book_id,))
    book = c.fetchone()

    c.execute("SELECT image_path FROM book_images WHERE book_id = ?", (book_id,))
    image_path = c.fetchone()[0]

    c.execute("SELECT price FROM book_prices WHERE book_id = ?", (book_id,))
    price = c.fetchone()[0]
    conn.close()

    for widget in frame_details.winfo_children():
        widget.destroy()

    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((150, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image_label = tk.Label(frame_details, image=photo, bg='#B5CFB7')
        image_label.image = photo
        image_label.pack()

    title_label = tk.Label(frame_details, text=f"Title: {book[0]}", font=('Arial', 14), bg='#B5CFB7')
    title_label.pack(anchor='w')

    author_label = tk.Label(frame_details, text=f"Author: {book[1]}", font=('Arial', 14), bg='#B5CFB7')
    author_label.pack(anchor='w')

    year_label = tk.Label(frame_details, text=f"Year: {book[2]}", font=('Arial', 14), bg='#B5CFB7')
    year_label.pack(anchor='w')

    genre_label = tk.Label(frame_details, text=f"Genre: {book[3]}", font=('Arial', 14), bg='#B5CFB7')
    genre_label.pack(anchor='w')

    pages_label = tk.Label(frame_details, text=f"Pages: {book[4]}", font=('Arial', 14), bg='#B5CFB7')
    pages_label.pack(anchor='w')

    price_label = tk.Label(frame_details, text=f"Price: {price}", font=('Arial', 14), bg='#B5CFB7')
    price_label.pack(anchor='w')

    button_frame = tk.Frame(frame_details, bg='#B5CFB7')
    button_frame.pack(anchor='w', pady=5)

    decrease_button = tk.Button(button_frame, text="-", command=lambda: decrease_quantity(book_id), font=('Arial', 12))
    decrease_button.pack(side='left', padx=(0, 10))

    add_to_cart_button = tk.Button(button_frame, text="Add to Cart", command=lambda: add_to_cart(book_id, 1, user_id), font=('Arial', 12))
    add_to_cart_button.pack(side='left', padx=(10, 10))

    increase_button = tk.Button(button_frame, text="+", command=lambda: increase_quantity(book_id), font=('Arial', 12))
    increase_button.pack(side='left', padx=(10, 0))

# Setting up the main Tkinter window
root = tk.Tk()
root.title("Bookstore")
root.geometry('1150x700+200+50')
root.resizable(False, False)

# Create a canvas for drawing
canvas = Canvas(root, width=1150, height=700, bd=0, highlightthickness=0)
canvas.pack(fill='both', expand=True)

# Draw frames with rounded corners
create_rounded_rectangle(canvas, 5, 5, 350, 700, r=20, fill='#B5CFB7', outline='#B5CFB7')
create_rounded_rectangle(canvas, 360, 10, 1120, 400, r=20, fill='#F6F5F2', outline='#F6F5F2')
create_rounded_rectangle(canvas, 360, 410, 1120, 700, r=20, fill='#F6F5F2', outline='#F6F5F2')

# Frame for displaying images
frame_images1 = Frame(root)
canvas.create_window(370, 30, anchor="nw", window=frame_images1)

frame_images3 = Frame(root)
canvas.create_window(370, 420, anchor="nw", window=frame_images3)

frame_images2 = Frame(root)
canvas.create_window(370, 200, anchor="nw", window=frame_images2)

# Frame for displaying book details
frame_details = Frame(root, bg='#B5CFB7', pady=50)
canvas.create_window(10, 10, anchor="nw", window=frame_details)

# Frame for displaying the cart
cart_frame = Frame(root, bg='#B5CFB7')
canvas.create_window(10, 600, anchor="nw", window=cart_frame)

# Load book data from the database
conn = sqlite3.connect(DATABASE_NAME)
c = conn.cursor()
c.execute("SELECT id, title FROM books")
books = c.fetchall()

c.execute("SELECT book_id, image_path FROM book_images")
book_images = c.fetchall()
conn.close()

# List to store image references to avoid garbage collection
photo_refs = []

# Add buttons for books with images
for i, (book_id, image_path) in enumerate(book_images):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        img = img.resize((100, 150), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        photo_refs.append(photo)  # Save the reference

        # Distribute buttons across frame_images1, frame_images2, and frame_images3
        if i < 5:
            frame = frame_images1
        elif i < 10:
            frame = frame_images2
        else:
            frame = frame_images3

        button = tk.Button(frame, image=photo, command=lambda book_id=book_id: show_book_details(book_id))
        button.pack(side='left', padx=10, pady=10)

# Go to Checkout function
def go_to_checkout():
    if len(cart) == 0:
        tk.messagebox.showinfo("Cart is Empty", "Your cart is empty. Please add books before proceeding to checkout.")
        return

    root.destroy()
    import appi
    appi.show_frame()

go_to_checkout_button = tk.Button(root, text="Go to Checkout", command=go_to_checkout, font=('Arial', 15))
go_to_checkout_button.place(relx=1.0, rely=1.0, anchor='se', x=-25, y=-40)

# Start the application
root.mainloop()
