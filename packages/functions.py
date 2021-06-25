import mysql.connector
from tkinter import *

def login():
    from tkinter import font

    def check():
        user = user_txt.get()
        pwd = pwd_txt.get()
        askpwd = 0
        while askpwd == 0:
            try:
                global db
                db = mysql.connector.connect(host='localhost', user=user, password=pwd)
                askpwd = 1
                pwd_prompt.destroy()
            except:
                try_lbl = Label(pwd_prompt, text="Try again!", fg="#fb3934", font=('Tw Cen MT', 11))
                try_lbl.place(x=110, y=205)
                print("Try again!")
                break

    def create():
        def rootcheck():
            username = user_txt.get()
            userpwd = pwd_txt.get()
            rootpwd = root_txt.get()
            askroot = 0
            while askroot == 0:
                try:
                    rootdb = mysql.connector.connect(host='localhost', user='root', password=rootpwd)
                    print("Success!")
                    askroot = 1
                    rootcur = rootdb.cursor()
                    rootcur.execute("CREATE USER '" + username + "'@'localhost' IDENTIFIED BY '" + userpwd + "';")
                    rootcur.execute("GRANT ALL PRIVILEGES ON * . * TO '" + username + "'@'localhost';")
                    rootpass.destroy()
                    check()
                    break
                except:
                    roottry_lbl = Label(rootpass, text="Try again!\n\nMake sure to set a unique username and\npassword in the previous window.", fg="#fb3934", font=('Tw Cen MT', 11))
                    roottry_lbl.place(x=0, y=125)
                    print("Try again!")
                    break


        rootpass = Tk()
        rootpass.iconbitmap("assets/key.ico")
        rootpass.geometry("255x200+572+340")
        rootpass.title("Root Pass")
        rootpass.tk_setPalette(background="#282828", foreground="#ebdbb2")

        roothead = Label(rootpass, text="Please enter your MySQL root password", font=('Tw Cen MT', 11))
        roothead.place(x=1, y=10)

        root_txt = Entry(rootpass, bd=1, show="*")
        root_txt.place(x=63, y=50)
        create_acc_btn = Button(rootpass, text="Create User", font=('Tw Cen MT', 11), command=rootcheck)
        create_acc_btn.place(x=83, y=90)

        rootpass.mainloop()



    pwd_prompt = Tk()
    pwd_prompt.iconbitmap("assets/loginicon.ico")
    pwd_prompt.geometry("300x250+550+300")
    pwd_prompt.title("Account Login")
    pwd_prompt.tk_setPalette(background="#282828", foreground="#ebdbb2")
    defaultFont = font.nametofont("TkDefaultFont")
    defaultFont.configure(family="Tw Cen MT", size=14)

    header = Label(pwd_prompt, text="MySQL Login", font=('Bahnschrift', 20), fg="#83a598")
    header.place(x=70, y=15)

    user_lbl = Label(pwd_prompt, text="Username")
    user_lbl.place(x=35, y=70)
    user_txt = Entry(pwd_prompt, bd=1)
    user_txt.place(x=130, y=75)

    pwd_lbl = Label(pwd_prompt, text="Password")
    pwd_lbl.place(x=35, y=110)
    pwd_txt = Entry(pwd_prompt, show="*", bd=1)
    pwd_txt.place(x=130, y=115)

    or_lbl = Label(pwd_prompt, text="or", font=("Tw Cen MT", 9))
    or_lbl.place(x=138, y=170)

    login_btn = Button(pwd_prompt, text="Login", font=('Tw Cen MT', 11), width=8, command=check)
    login_btn.place(x=60,y=167)

    create_btn = Button(pwd_prompt, text="Create", font=('Tw Cen MT', 11), width=8, command=create)
    create_btn.place(x=160,y=167)

    pwd_prompt.mainloop()