import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import dbfinl
DATABASE_NAME = 'dbfinl.db'


def on_entry_click1(event):
    if phonentry.get() == '+20 ':
        phonentry.delete(0, tk.END)
        phonentry.config(fg='black')


def on_focusout1(event):
    if phonentry.get() == '':
        phonentry.insert(0, '+20 ')
        phonentry.config(fg='grey')


def on_entry_click2(event):
    if mailentry.get() == '@gmail.com':
        mailentry.delete(0, tk.END)
        mailentry.config(fg='black')


def on_focusout2(event):
    if mailentry.get() == '':
        mailentry.insert(0, '@gmail.com')
        mailentry.config(fg='grey')


def on_entry_click3(event):
    if locationentry.get() == 'location / street name and landmark for the house..':
        locationentry.delete(0, tk.END)
        locationentry.config(fg='black')


def on_focusout3(event):
    if locationentry.get() == '':
        locationentry.insert(
            0, 'location / street name and landmark for the house..')
        locationentry.config(fg='grey')


def create_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    canvas.create_oval(x1, y1, x1 + r * 2, y1 + r * 2, **kwargs)
    canvas.create_oval(x2 - r * 2, y1, x2, y1 + r * 2, **kwargs)
    canvas.create_oval(x1, y2 - r * 2, x1 + r * 2, y2, **kwargs)
    canvas.create_oval(x2 - r * 2, y2 - r * 2, x2, y2, **kwargs)
    canvas.create_rectangle(x1 + r, y1, x2 - r, y2, **kwargs)
    canvas.create_rectangle(x1, y1 + r, x2, y2 - r, **kwargs)


def get_current_user_id():
   
    return 2


def display_order(user_id):
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()
    try:
        c.execute(
            "SELECT book_id, quantity FROM cart WHERE user_id = ?", (user_id,))
        cart_items = c.fetchall()

        if not cart_items:
            messagebox.showinfo("Info", "Your cart is empty.")
            return

        for row in tree.get_children():
            tree.delete(row)

        total_price = 0

        for book_id, quantity in cart_items:
            c.execute('''
            SELECT books.title, book_prices.price 
            FROM books 
            JOIN book_prices ON books.id = book_prices.book_id
            WHERE books.id = ?''', (book_id,))
            book = c.fetchone()
            if book:
                title, price = book
                total_price += price * quantity
                tree.insert("", tk.END, values=(title, quantity,
                            f"{price:.2f}", f"{price * quantity:.2f}"))

        total_label.config(text=f"Total Price: {total_price:.2f}")

        c.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        con.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        con.close()


def save_order_to_database(user_id):
    con = sqlite3.connect(DATABASE_NAME)
    c = con.cursor()

    phone = phonentry.get()
    email = mailentry.get()
    city = combo.get()
    location = locationentry.get()
    building_number = buildnum.get()
    floor_number = floornum.get()

    c.execute("SELECT full_name FROM userinfo WHERE user_id = ?", (user_id,))
    existing_user = c.fetchone()

    if existing_user:
        c.execute('''
        UPDATE userinfo
        SET phone = ?, email = ?, city = ?, location = ?, building_number = ?, floor_number = ?
        WHERE user_id = ?''', (phone, email, city, location, building_number, floor_number, user_id))
    else:
        c.execute('''
        INSERT INTO userinfo (user_id, full_name, phone, email, city, location, building_number, floor_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (user_id, firstname.get(), phone, email, city, location, building_number, floor_number))

    con.commit()
    con.close()


root = tk.Tk()
root.title("Bookstore")
root.geometry('1150x700+200+50')
root.resizable(False, False)

canvas = tk.Canvas(root, width=1150, height=700,
                   bg='white', bd=0, highlightthickness=0)
canvas.pack(fill='both', expand=True)

frame = create_rounded_rectangle(
    canvas, 5, 5, 670, 700, r=20, fill='#B5CFB7', outline='#B5CFB7')
framright = create_rounded_rectangle(
    canvas, 680, 5, 1140, 690, r=20, fill='#F6F5F2', outline='#F6F5F2')

bill = tk.Label(frame, text="Bill and Shipping",
                font=('Gupter', 18, 'bold'), bg="#B5CFB7")
bill.place(x=30, y=10)

frname = tk.Label(frame, text="Full Name", font=('Gupter', 18,), bg="#B5CFB7")
frname.place(x=8, y=50)
firstname = tk.Entry(frame, width=30,)
firstname.place(x=150, y=55)

phone = tk.Label(frame, text="Phone", font=('Gupter', 18,), bg="#B5CFB7")
phone.place(x=10, y=90)
phonentry = tk.Entry(frame, width=20,)
phonentry.insert(0, '+20 ')
phonentry.bind('<FocusIn>', on_entry_click1)
phonentry.bind('<FocusOut>', on_focusout1)
phonentry.place(x=150, y=90)

Email = tk.Label(frame, text="Email", font=('Gupter', 18,), bg="#B5CFB7")
Email.place(x=10, y=130)
mailentry = tk.Entry(frame, width=33,)
mailentry.insert(0, '@gmail.com')
mailentry.bind('<FocusIn>', on_entry_click2)
mailentry.bind('<FocusOut>', on_focusout2)
mailentry.place(x=150, y=130)

City = tk.Label(frame, text="City", font=('Gupter', 18,), bg="#B5CFB7")
City.place(x=10, y=170)
cities = ['Cairo', 'Alexandria', 'Giza', 'Port Said', 'Aswan', 'Suez', 'Tanta', 'Asyut', 'Fayyum', 'Sohag',
          'Matareya', 'Akhmim', 'Qalyub', 'Idfu', 'Arish', 'Banha', 'Shibin El Kom', '6th of October City']
combo = ttk.Combobox(frame, values=cities, state='readonly')
combo.place(x=150, y=170)

location = tk.Label(frame, text="Location", font=('Gupter', 18,), bg="#B5CFB7")
location.place(x=10, y=210)
locationentry = tk.Entry(frame, width=50,)
locationentry.insert(0, 'location / street name and landmark for the house..')
locationentry.bind('<FocusIn>', on_entry_click3)
locationentry.bind('<FocusOut>', on_focusout3)
locationentry.place(x=150, y=210)

bldnum = tk.Label(frame, text="Building Number",
                  font=('Gupter', 18,), bg="#B5CFB7")
bldnum.place(x=10, y=250)
buildnum = tk.Entry(frame, width=20,)
buildnum.place(x=200, y=260)

flnum = tk.Label(frame, text="Floor Number",
                 font=('Gupter', 18,), bg="#B5CFB7")
flnum.place(x=360, y=250)
floornum = tk.Entry(frame, width=20,)
floornum.place(x=520, y=260)

#imgimg = tk.PhotoImage(file="C:/Users/Noran Ali/Desktop/Python2/img/checkout2.png")
#imgg = imgimg.subsample(4, 5)

lblimg = tk.Label(frame, bg='#B5CFB7')
lblimg.place(x=60, y=320)

columns = ('Title', 'Quantity', 'Price', 'Total')
tree = ttk.Treeview(framright, columns=columns, show='headings', height=20)

total_width = 430
num_columns = len(columns)
column_width = total_width // num_columns

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=column_width, anchor='center')

tree.place(x=700, y=70, width=total_width, height=400)

total_label = tk.Label(framright, font=("italic", 15), bg='#F6F5F2')
total_label.place(x=700, y=700)


def complete_process():
    user_id = get_current_user_id()
    display_order(user_id)
    save_order_to_database(user_id)


btn1 = tk.Button(frame, text='Complete Process', fg='black', bg='white',
                 width=16, height=1, font=('tahoma', 10, 'bold'), command=complete_process)
btn1.place(anchor='center', x=200, y=320)


def back():
    root.destroy()
    import homeframe
    homeframe.show_frame()


btn2 = tk.Button(frame, text='Keep Shopping', fg='black', bg='white',
                 width=15, height=1, font=('tahoma', 10, 'bold'), command=back)
btn2.place(anchor='center', x=420, y=320)

paymentlbl = tk.Label(framright, text='Payment', font=("italic", 25))
paymentlbl.place(x=860, y=20)

root.mainloop()
