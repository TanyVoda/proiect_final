from functools import partial
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import main
from User import User


class RegisterPage(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.geometry('350x320')
        self.title('Interfata de register')
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.bg = ImageTk.PhotoImage(Image.open("images\\funny_login2.jpg"))
        label1 = Label(self, image=self.bg)
        label1.pack(fill=BOTH, expand=1)
        label1.grid_columnconfigure(0, weight=1)

        usernameLabelR = Label(label1, bg='#64e1e8', text="User Name")
        usernameLabelR.grid(row=0, column=0, pady=(220,0), padx=(20,0), sticky=W)
        usernameLabelR.config(font=('Comic Sans MS', 10, 'bold'))
        user = StringVar()
        usernameEntryR = Entry(label1, bg='#64e1e8', justify='center', textvariable=user)
        usernameEntryR.grid(row=0, column=1, pady=(220,0), padx=(0, 80))
        usernameEntryR.config(font=('Comic Sans MS', 10, 'bold'))
        passwordLabel = Label(label1, bg='#64e1e8', text="Password")
        passwordLabel.grid(row=1, column=0, padx=(20,0), sticky=W)
        passwordLabel.config(font=('Comic Sans MS', 10, 'bold'))
        passs = StringVar()
        passwordEntryR = Entry(label1, bg='#64e1e8', justify='center', textvariable=passs, show='•')
        passwordEntryR.grid(row=1, column=1, padx=(0, 80), pady=(0, 10))
        passwordEntryR.config(font=('Comic Sans MS', 10, 'bold'))
        register = partial(label1.register, user, passs)
        loginButton = Button(label1, bg='#64e1e8', text="Register", command=register)
        loginButton.grid(row=4, column=1, padx=(0, 20), sticky=W)
        loginButton.config(font=('Comic Sans MS', 10, 'bold'))
        button2Click = partial(self.button2Click)
        button2 = Button(label1, bg='#64e1e8', text="Cancel", command=button2Click)
        button2.grid(row=4, column=1, padx=(0, 100), sticky=E)
        button2.config(font=('Comic Sans MS', 10, 'bold'))

    def register(self, username, password):
        print(username.get(), password.get())
        if len(username.get()) < 3:
            messagebox.showerror("ERROR", "Numele de utilizator este prea scurt (<3 caractere)!")
            return
        if len(password.get()) < 5:
            messagebox.showerror("ERROR", "Parola este prea scurta (<5 caractere)!")
            return
        u = User(username.get(), password.get())
        main.list.append(u)
        sql = "INSERT INTO users(user, password) VALUES (%s, %s)"
        val = (f"{u.username}",f"{u.password}")
        main.mycursor.execute(sql,val)
        main.mydb.commit()
        print(main.mycursor.lastrowid)
        messagebox.showinfo("INFO", f"Userul {u.username} a fost adaugat cu succes")
        self.master.deiconify()
        self.destroy()


    def button2Click(self):
        self.master.deiconify()
        self.destroy()
        return


