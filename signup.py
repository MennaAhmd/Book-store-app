from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sqlite3
import dbfinl  # Import the database module

# Initialize the database
dbfinl.setup_database()

screen = Tk()
screen.title('Sign Up')
screen.geometry('660x700+400+50')
screen.resizable(False, False)
screen.config(bg='white')

imgSP = PhotoImage(file="D:/Desktop/Book store project/img/sginup.png")
####SignUp Image
framesp = Frame(screen, bg='white', width=700, height=700)
lblimg = Label(framesp, bg='white', image=imgSP)

def entfull(e):
    if txtfull.get() == 'Full Name':
        txtfull.delete(0, 'end')

def leavefull(e):
    full = txtfull.get()
    if full == '':
        txtfull.insert(0, 'Full Name')

def entusr(e):
    if txtusr.get() == 'Username':
        txtusr.delete(0, 'end')

def leaveusr(e):
    usr = txtusr.get()
    if usr == '':
        txtusr.insert(0, 'Username')

def entpas(e):
    if txtpas.get() == 'Password':
        txtpas.delete(0, 'end')
        #txtpas.config(fg='black', show='*')

def leavepas(e):
    fir = txtpas.get()
    if fir == '':
        txtpas.insert(0, 'Password')

def entpss(e):
    if txtpss.get() == 'Confirm Password':
        txtpss.delete(0, 'end')
        #txtpas.config(fg='black', show='*')

def leavepss(e):
    pss = txtpss.get()
    if pss == '':
        txtpss.insert(0, 'Confirm Password')
        

def register_user():
    full_name = txtfull.get()
    username = txtusr.get()
    password = txtpas.get()
    confirm_password = txtpss.get()
    
    if full_name == 'Full Name' or username == 'Username' or password == 'Password' or confirm_password == 'Confirm Password':
        messagebox.showerror("Error", "Please fill out all fields.")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
    else:
        try:
            dbfinl.register_user(full_name, username, password)
            messagebox.showinfo("Success", "Registration successful!")
            txtfull.delete(0, END)
            txtusr.delete(0, END)
            txtpas.delete(0, END)
            txtpss.delete(0, END)
            txtfull.insert(0, 'Full Name')
            txtusr.insert(0, 'Username')
            txtpas.insert(0, 'Password')
            txtpss.insert(0, 'Confirm Password')
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
txtfull = Entry(framesp, width=22, font=('Arial', 12), border=0, fg='black', insertbackground='black')
txtusr = Entry(framesp, width=22, font=('Arial', 12), border=0, fg='black', insertbackground='black')
txtpas = Entry(framesp, width=22, font=('Arial', 12), border=0, fg='black', insertbackground='black')
txtpss = Entry(framesp, width=22, font=('Arial', 12), border=0, fg='black', insertbackground='black')

framesp.place(anchor='center', relx=0.5, rely=0.5)
lblimg.place(anchor='center', relx=0.5, rely=0.5)

txtfull.place(x=218, y=270)
txtfull.insert(0, 'Full Name')
txtfull.bind('<FocusIn>', entfull)
txtfull.bind('<FocusOut>', leavefull)

txtusr.place(x=218, y=320)
txtusr.insert(0, 'Username')
txtusr.bind('<FocusIn>', entusr)
txtusr.bind('<FocusOut>', leaveusr)

txtpas.place(x=218, y=370)
txtpas.insert(0, 'Password')
txtpas.bind('<FocusIn>', entpas)
txtpas.bind('<FocusOut>', leavepas)

txtpss.place(x=218, y=420)
txtpss.insert(0, 'Confirm Password')
txtpss.bind('<FocusIn>', entpss)
txtpss.bind('<FocusOut>', leavepss)

def login():
    screen.destroy()
    import login
    login.show_frame()

btnSI = Button(framesp, width=4, text='Sign In', bg='#d3f4dc', fg='black', relief='flat', cursor='hand2', command=login)
lblsp = Label(framesp, text='Already a member?', fg='#72b385', bg='#d3f4dc')
btnr = Button(framesp, width=29, text='Register', bg='#92e3a9', fg='white', cursor='hand2', height=2, font=('bold', 9), command=register_user)

lblsp.place(x=245, y=452)
btnSI.place(x=353, y=450)
btnr.place(x=217, y=478)

screen.mainloop()
