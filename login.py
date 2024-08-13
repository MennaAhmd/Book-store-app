# -- coding: utf-8 --
"""
Created on Sun Aug  4 19:26:54 2024

@author: Noran Ali
"""


from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import dbfinl  # Import the database module

# Initialize the database
dbfinl.setup_database()

# Global variables
root = Tk()
root.title("Login")
root.geometry('900x600+300+110')
root.resizable(False, False)
#root.iconbitmap("C:/Users/Noran Ali/Desktop/Python2/img/user.ico")
root['bg'] = 'white'

img = PhotoImage(file="D:/Desktop/Book store project/img/login.png")

# Functions for entry field behavior
def entEmail(e):
    if txt2.get() == 'Username':
        txt2.delete(0, 'end')

def leaveEmail(e):
    if txt2.get() == '':
        txt2.insert(0, 'Username')

def entPass(e):
    if txt3.get() == 'Password':
        txt3.delete(0, 'end')

def leavePass(e):
    if txt3.get() == '':
        txt3.insert(0, 'Password')

def login():
    username = txt2.get()
    password = txt3.get()
    user_id = dbfinl.login_user(username, password)
    if user_id:
        messagebox.showinfo("Login", "Login successful!")
        root.destroy()
        import homeframe
        homeframe.show_frame()
    else:
        messagebox.showerror("Login", "Invalid username or password.")

# Setup login interface
frm1 = Frame(root, bg='white', width=500, height=450)
lbl = Label(root, bg='white', image=img)
lbl1 = Label(root, text='Sign in', font=('Microsoft YaHei UI Light', 40), bg='white', fg='black')

txt2 = Entry(frm1, width=40, bg='white', fg='black', border=0, font=('bold', 13))
framm = Frame(root, width=250, bg='black', height=2)

txt3 = Entry(frm1, width=40, bg='white', fg='black', border=0, font=('bold', 13))
frammm = Frame(root, width=250, bg='black', height=2)

frm1.place(anchor='center', relx=0.5, rely=0.5, x=120, y=100)
lbl.place(x=30, y=80)
lbl1.place(x=550, y=100)

txt2.place(x=200, y=79)
txt2.insert(0, 'Username')
txt2.bind('<FocusIn>', entEmail)
txt2.bind('<FocusOut>', leaveEmail)
framm.place(x=520, y=278)

txt3.place(x=200, y=139)
txt3.insert(0, 'Password')
txt3.bind('<FocusIn>', entPass)
txt3.bind('<FocusOut>', leavePass)
frammm.place(x=520, y=338)

def signup():
    root.destroy()
    import signup
    signup.show_frame()

btn = Button(frm1, text='Sign In', font=('bold', 12), width=20, height=2, bg='#72b385', fg='black', cursor='hand2', command=login)
lblSP = Label(frm1, text='Don\'t have an account?', bg='white', fg='black', font=('bold', 11))
btnSP = Button(frm1, text='Sign Up', font=('bold, underlined', 10), width=5, bg='white', fg='#72b385', cursor='hand2', relief='flat', command=signup)

btn.place(x=230, y=200)
lblSP.place(x=218, y=275)
btnSP.place(x=378, y=272)

root.mainloop()