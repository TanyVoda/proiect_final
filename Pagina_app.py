from tkinter import *
from tkinter import messagebox
import main
import datetime
import webbrowser


class PaginaUser(Toplevel):
    def __init__(self):
        super().__init__()
        self.startstop = True
        self.selector_click = 0
        self.geometry("800x900")
        self.minsize(800,900)
        self.title("Account Login")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        text_titlu = "Bine ai venit " + main.user.upper() + ", in jos gasesti lista ta de produse"
        labelMesaj = Label(self, text=text_titlu, bg="#64e1e8",font=('Comic Sans MS', 15, 'bold'))
        labelMesaj.grid(row=0, columnspan=4, pady=(0,20), sticky=W+E)
        self.linkulDeMonitorizat = Text(self, height=8, borderwidth=3)
        self.linkulDeMonitorizat.grid(row=1, columnspan=4, pady=(0,20))
        self.linkulDeMonitorizat.bind("<Button-1>", self.click)
        self.linkulDeMonitorizat.bind("<Leave>", self.leave)
        self.linkulDeMonitorizat.config(font=('Comic Sans MS', 10, 'bold'))
        self.linkulDeMonitorizat.tag_configure('tag-center', justify='center')
        self.linkulDeMonitorizat.insert(END, "Introdu linkul produsului pe il monitorizezi", 'tag-center')
        self.linkulDeMonitorizat.tag_add("center", 1.0, "end")

        self.photoButton = PhotoImage(file=r"images\\search_button.png")
        self.photoimageButton = self.photoButton.subsample(2, 2)
        buttonSearch = Button(self, bg='#64e1e8', text="Search", image=self.photoimageButton, compound=LEFT, height=30, font =('Comic Sans MS', 10, 'bold'),  command=self.verificaSiteu)
        buttonSearch.grid(row=2, column=0, padx=15, pady=(0,15), sticky=W+E)

        self.photoButtonDeleteAll = PhotoImage(file=r"images\\delete_all.png")
        self.photoimageButtonDeleteAll = self.photoButtonDeleteAll.subsample(2, 2)
        delete_all = Button(self, bg='#64e1e8', text=" Sterge Toata Lista", image = self.photoimageButtonDeleteAll, height=30, compound=LEFT, font =('Comic Sans MS', 10, 'bold'), command=self.sterge_lista)
        delete_all.grid(row=2, column=1, padx=18, pady=(0,15), sticky=E+W)

        self.frame_listbox = Frame(self, borderwidth=5, highlightbackground="#64e1e8", highlightthickness=2, highlightcolor="#64e1e8", background="white")
        self.frame_listbox.grid(row=3, columnspan=2, padx=15, sticky=W + E)
        self.frame_listbox.grid_columnconfigure(0, weight=1)

        self.listBox_produse = Listbox(self.frame_listbox, font=('Comic Sans MS', 10, 'bold'),  borderwidth=0, highlightthickness=0)
        scrollbar = Scrollbar(self.frame_listbox)
        scrollbar.grid(row=0, column=3,pady=(10,0), sticky=N+S)
        main.mycursor.execute(f"SELECT * FROM datesite WHERE user = '{main.user}'")
        result = main.mycursor.fetchall()
        self.counter = 0
        for link in result:
            self.counter += 1
            self.listBox_produse.insert(self.counter, link[2])
        self.listBox_produse.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listBox_produse.yview)
        self.listBox_produse.bind("<<ListboxSelect>>", self.callback)
        self.listBox_produse.grid(row=0, columnspan=2, padx=(10,0), pady=(10,0), sticky=W + E)

        self.frameCnt = 29
        self.frames = [PhotoImage(file="images\\spaceballs.gif",format='gif -index %i' % (i)) for i in range(self.frameCnt)]
        self.label848 = Label(self)

        self.frameCnt1 = 19
        self.frames1 = [PhotoImage(file="images\\cY0.gif",format='gif -index %i' % (i)) for i in range(self.frameCnt1)]

        self.bind("<FocusOut>", self.quit)

    def update1(self, ind):
        try:
            self.label848.grid(row=7, column=0)
        except:
            self.label848 = Label(self)
            self.label848.grid(row=7, column=0)
        frame = self.frames1[ind]
        ind += 1
        if ind == self.frameCnt1:
            ind = 0
        self.label848.configure(image=frame)
        if self.startstop == False:
            self.after(40, self.update1, ind)
        else:
            self.label848.grid_forget()


    def update2(self, ind):
        try:
            self.label848.grid(row=7, column=0, columnspan=4)
        except:
            self.label848 = Label(self)
            self.label848.grid(row=7, column=0, columnspan=4)
        frame = self.frames[ind]
        ind += 1
        if ind == self.frameCnt:
            ind = 0
        self.label848.configure(image=frame)
        if self.startstop == False:
            self.after(40, self.update2, ind)
        else:
            self.label848.grid_forget()

    def click(self, event):
        self.linkulDeMonitorizat.delete("1.0", "end")

    def leave(self, event):
        if len(self.linkulDeMonitorizat.get("1.0", "end")) > 1:
            pass
        else:
            self.linkulDeMonitorizat.delete("1.0", "end")
            self.linkulDeMonitorizat.tag_configure('tag-center', justify='center')
            self.linkulDeMonitorizat.insert("1.0", 'Introdu linkul produsului pe il monitorizezi', 'tag-center')
            self.linkulDeMonitorizat.tag_add("center", 1.0, "end")

    def openweb(self, url):
        webbrowser.open(url, new=1)

    def afiseaza_pret_mic(self, titlu):
        from siteuriSearch import pretCelMic
        detalii_cel_mai_mic = pretCelMic.scaneazaPagina(titlu)
        if detalii_cel_mai_mic != None:
            try:
                self.label_pret_mic.destroy()
                self.buttonOpenUrl.destroy()
            except:
                pass
            self.startstop = False
            self.after(0, self.update1, 0)
            text_pret_mic = "Psssst....\nAm gasit produsul cautat de tine la " + str(detalii_cel_mai_mic[0]) + "\nCe zici?\nDaca vrei sa il cumperi...\nAi button special pentru tine care te duce pe site!"
            self.label_pret_mic = Label(self, text=text_pret_mic, font =('Comic Sans MS', 10, 'bold'))
            self.label_pret_mic.grid(row=7, column=1, sticky="n")

            self.buttonOpenUrlImg = PhotoImage(file=r"images\\hurry.png")
            self.buttonOpenUrlImg = self.buttonOpenUrlImg.subsample(2, 2)
            self.buttonOpenUrl = Button(self, bg='#64e1e8', text=" GoGoGo", image=self.buttonOpenUrlImg, compound=LEFT, height=30, font =('Comic Sans MS', 10, 'bold'), command=lambda : self.openweb(detalii_cel_mai_mic[1]))
            self.buttonOpenUrl.grid(row=7,column=1,pady=(15,15),sticky='s')
        else:
            try:
                self.label_pret_mic.destroy()
                self.buttonOpenUrl.destroy()
            except:
                pass
            self.startstop = False
            self.after(0, self.update2, 0)

    def callback(self, event):
        selection = self.listBox_produse.curselection()
        if selection:
            if self.selector_click != selection[0]:
                self.startstop = True
            try:
                self.label848.grid_forget()
            except:
                pass
            try:
                self.label_select_titlu.destroy()
            except:
                pass
            try:
                self.label_select_pret.destroy()
            except:
                pass
            try:
                self.label_text_reverificare.destroy()
            except:
                pass
            try:
                self.label_pret_mic.destroy()
            except:
                pass
            try:
                self.buttonOpenUrl.destroy()
            except:
                pass
            index = selection[0]
            self.selector_click = index
            data = self.listBox_produse.get(index)
            print(data)
            self.label_text_reverificare = Label(self, text="Ati selectat:", font=('Comic Sans MS', 10, 'bold'), bg="#64e1e8")
            self.label_text_reverificare.config(anchor=CENTER)
            self.label_text_reverificare.grid(row=4, column=0, padx=(15,0), sticky=W+E)

            self.label_text_pret = Label(self, text="La pretul de:", font=('Comic Sans MS', 10, 'bold'), bg="#64e1e8")
            self.label_text_pret.config(anchor=CENTER)
            self.label_text_pret.grid(row=5, column=0, padx=(15,0), sticky=W+E)
            data_de_afisat = data
            if len(data_de_afisat) > 50:
                data_de_afisat = data_de_afisat[:50]
                data_de_afisat = data_de_afisat + "....."
            self.label_select_titlu = Label(self, text=data_de_afisat, font=('Comic Sans MS', 10, 'bold'), bg="#64e1e8")
            self.label_select_titlu.grid(row=4, column=1, padx=(0,15), sticky=W+E)
            main.mycursor.execute(f"SELECT pret FROM datesite WHERE user='{main.user}' and titlu_produs='{data}'")
            pret_afisaz = main.mycursor.fetchall()
            print(pret_afisaz)
            self.label_select_pret = Label(self, text=pret_afisaz, font=('Comic Sans MS', 10, 'bold'), bg="#64e1e8")
            self.label_select_pret.grid(row=5, column=1, padx=(0,15), sticky=W+E)

            self.buttonPretMicImg = PhotoImage(file=r"images\\web.png")
            self.buttonPretMicImg = self.buttonPretMicImg.subsample(2, 2)
            buttonPretMic = Button(self, bg='#64e1e8', text=" Vezi cel mai mic pret de pe net pentru produsul tau", image=self.buttonPretMicImg, compound=LEFT, height=30, font =('Comic Sans MS', 10, 'bold'), command=lambda : self.afiseaza_pret_mic(data))
            buttonPretMic.grid(row=6, column=0, pady=(15, 20), padx=(15, 20))

            self.buttonStergeProdusulImg = PhotoImage(file=r"images\\delete.png")
            self.buttonStergeProdusulImg = self.buttonStergeProdusulImg.subsample(2, 2)
            buttonStergeProdusul = Button(self, bg='#64e1e8', text=" Sterge produsul din lista", image=self.buttonStergeProdusulImg, compound=LEFT, height=30, font =('Comic Sans MS', 10, 'bold'), command=lambda: self.sterge_produsul(data, index))
            buttonStergeProdusul.grid(row=6, column=1, pady=(15, 20))
        else:
            self.label_select_titlu.configure(text="")

    def sterge_produsul(self, data, index):
        main.mycursor.execute(f"DELETE FROM datesite WHERE user='{main.user}' and titlu_produs='{data}'")
        main.mydb.commit()
        self.listBox_produse.delete(index,index)

    def sterge_lista(self):
        main.mycursor.execute(f"DELETE FROM datesite WHERE user='{main.user}'")
        main.mydb.commit()
        main.mycursor.execute(f"ALTER TABLE datesite AUTO_INCREMENT = 1")
        self.listBox_produse.delete(0,END)

    def verificaSiteu(self):
        link = self.linkulDeMonitorizat.get("1.0", END).strip()
        if "emag" in link.lower():
            from siteuriSearch import Emag
            detalii_emag = Emag.scaneazaPagina(link)
            self.linkulDeMonitorizat.delete("1.0", END)
            main.mycursor.execute(f"SELECT * FROM datesite WHERE link = '{link}'")
            result = main.mycursor.fetchall()
            if len(result) == 0:
                today_date = datetime.date.today().strftime("%d/%m/%Y")
                sql = "INSERT INTO datesite(link, titlu_produs, pret, user, data_search) VALUES (%s, %s, %s, %s, %s)"
                val = (f"{detalii_emag[0]}", f"{detalii_emag[1]}", f"{detalii_emag[2]}", f"{main.user}", f"{today_date}")
                main.mycursor.execute(sql, val)
                main.mydb.commit()
                print(main.mycursor.lastrowid)
                self.counter +=1
                self.listBox_produse.insert(self.counter, detalii_emag[1])
                root = Tk()
                root.withdraw()
                messagebox.showinfo("INFO", f"Produsul {detalii_emag[1]} a fost adaugat cu succes")
                root.destroy()
            else:
                root = Tk()
                root.withdraw()
                messagebox.showinfo("INFO", f"Produsul {detalii_emag[1]} exista deja in baza de date")
                root.destroy()
        elif "altex" in link.lower():
            from siteuriSearch import Altex
            detalii_altex = Altex.scaneazaPagina(link)
            self.linkulDeMonitorizat.delete("1.0", END)
            main.mycursor.execute(f"SELECT * FROM datesite WHERE link = '{link}'")
            result = main.mycursor.fetchall()
            if len(result) == 0:
                today_date = datetime.date.today().strftime("%d/%m/%Y")
                sql = "INSERT INTO datesite(link, titlu_produs, pret, user, data_search) VALUES (%s, %s, %s, %s, %s)"
                val = (f"{detalii_altex[0]}", f"{detalii_altex[1]}", f"{detalii_altex[2]}", f"{main.user}", f"{today_date}")
                main.mycursor.execute(sql, val)
                main.mydb.commit()
                print(main.mycursor.lastrowid)
                self.counter += 1
                self.listBox_produse.insert(self.counter, detalii_altex[1])
                root = Tk()
                root.withdraw()
                messagebox.showinfo("INFO", f"Produsul {detalii_altex[1]} a fost adaugat cu succes")
                root.destroy()
            else:
                root = Tk()
                root.withdraw()
                messagebox.showinfo("INFO", f"Produsul {detalii_altex[1]} exista deja in baza de date")
                root.destroy()
        elif "flanco" in link.lower():
            from siteuriSearch import Flanco
            detalii_flanco = Flanco.scaneazaPagina(link)
            self.linkulDeMonitorizat.delete("1.0", END)
            main.mycursor.execute(f"SELECT * FROM datesite WHERE link = '{link}'")
            result = main.mycursor.fetchall()
            if len(result) == 0:
                today_date = datetime.date.today().strftime("%d/%m/%Y")
                sql = "INSERT INTO datesite(link, titlu_produs, pret, user, data_search) VALUES (%s, %s, %s, %s, %s)"
                val = (f"{detalii_flanco[0]}", f"{detalii_flanco[1]}", f"{detalii_flanco[2]}", f"{main.user}", f"{today_date}")
                main.mycursor.execute(sql, val)
                main.mydb.commit()
                print(main.mycursor.lastrowid)
                self.counter += 1
                self.listBox_produse.insert(self.counter, detalii_flanco[1])
                root = Tk()
                root.withdraw()
                messagebox.showinfo("INFO", f"Produsul {detalii_flanco[1]} a fost adaugat cu succes")
                root.destroy()
            else:
                root = Tk()
                root.withdraw()
                messagebox.showinfo("INFO", f"Produsul {detalii_flanco[1]} exista deja in baza de date")
                root.destroy()
        else:
            root = Tk()
            root.withdraw()
            messagebox.showinfo("INFO", f"Linkul: {link}\n nu e valid")
            self.linkulDeMonitorizat.delete("1.0", END)
            root.destroy()








