from functools import partial
from tkinter import *
from tkinter import messagebox
from RegisterPage import RegisterPage
from Pagina_app import PaginaUser
import main
from PIL import ImageTk,Image


class LoginPage(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x400')
        self.title('Interfata de logare')
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.bg = ImageTk.PhotoImage(Image.open("images\\login_background.jpg"))
        label1 = Label(self, image=self.bg)
        label1.pack(fill=BOTH, expand=1)
        label1.grid_columnconfigure(0, weight=1)
        usernameLabel = Label(label1, bg='#64e1e8', text="User Name")
        usernameLabel.grid(row=0, column=0, pady=(20, 5))
        usernameLabel.config(font=('Comic Sans MS', 10, 'bold'))
        username = StringVar()
        usernameEntry = Entry(label1, bg='#64e1e8', justify='center', textvariable=username)
        usernameEntry.grid(row=1, column=0, pady=(0, 20))
        usernameEntry.config(font=('Comic Sans MS', 15, 'bold'))
        passwordLabel = Label(label1, bg='#64e1e8', text="Password")
        passwordLabel.grid(row=2, column=0, pady=(0, 5))
        passwordLabel.config(font=('Comic Sans MS', 10, 'bold'))
        password = StringVar()
        passwordEntry = Entry(label1, bg='#64e1e8', justify='center', textvariable=password, show='•')
        passwordEntry.grid(row=3, column=0, pady=(0, 20))
        passwordEntry.config(font=('Comic Sans MS', 15, 'bold'))
        validateLogin = partial(self.validateLogin, username, password)

        loginButton = Button(label1, bg='#64e1e8', text="Login", width=10, command=validateLogin)
        loginButton.grid(row=5, column=0, pady=(0, 50))
        loginButton.config(font=('Comic Sans MS', 10, 'bold'))
        button2 = Button(label1, bg='#64e1e8', text="Register", width=10, command=self.button2Click)
        button2.grid(row=7, column=0, sticky=E, padx=(0, 40))
        button2.config(font=('Comic Sans MS', 10, 'bold'))

    def validateLogin(self, user, password):

        main.mycursor.execute(f"SELECT PASSWORD FROM USERS WHERE User='{user.get()}'")
        result = main.mycursor.fetchall()

        if len(result) == 0:
            print("Wrong username")
            messagebox.showinfo("INFO", f"Username gresit!")
            return
        if password.get() == result[0][0]:
            print("succes")
            self.withdraw()
            main.user = user.get()
            login = PaginaUser()
            login.protocol("WM_DELETE_WINDOW", self.on_closing)
            login.grab_set()
        else:
            print("Wrong pass")
            messagebox.showinfo("INFO", f"Parola gresita!")
        print("username entered :", user.get())
        print("password entered :", password.get())
        return

    def on_closing(self):
        self.destroy()

    def button2Click(self):
        self.withdraw()
        register = RegisterPage(self)
        register.grab_set()
        self.iconify()
        return

