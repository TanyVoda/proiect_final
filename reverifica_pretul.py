import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bazaswiss"
)
mycursor = mydb.cursor()


def reverificaPretul():
    mycursor.execute(f"SELECT link, pret, titlu_produs FROM datesite WHERE 1")
    results = mycursor.fetchall()
    for var in results:
        if "emag" in var[0].lower():
            from siteuriSearch import Emag
            detalii_emag = Emag.scaneazaPagina(var[0])
            if detalii_emag[2] != var[1]:
                mycursor.execute(f"UPDATE datesite SET pret='{detalii_emag[2]}' WHERE titlu_produs='{var[2]}'")
                mycursor.fetchall()
                print("Am facut update la pret de la produsul " + str(var[2]))
            else:
                print("Produsul : \n " + str(var[2]) + "\nA ramas neschimbat!")
        elif "altex" in var[0].lower():
            from siteuriSearch import Altex
            detalii_altex = Altex.scaneazaPagina(var[0])
            if detalii_altex[2] != var[1]:
                mycursor.execute(f"UPDATE datesite SET pret='{detalii_altex[2]}' WHERE titlu_produs='{var[2]}'")
                mycursor.fetchall()
                print("Am facut update la pret de la produsul " + str(var[2]))
            else:
                print("Produsul : \n " + str(var[2]) + "\nA ramas neschimbat!")
        elif "flanco" in var[0].lower():
            from siteuriSearch import Flanco
            detalii_flanco = Flanco.scaneazaPagina(var[0])
            if detalii_flanco[2] != var[1]:
                mycursor.execute(f"UPDATE datesite SET pret='{detalii_flanco[2]}' WHERE titlu_produs='{var[2]}'")
                mycursor.fetchall()
                print("Am facut update la pret de la produsul " + str(var[2]))
            else:
                print("Produsul : \n " + str(var[2]) + "\nA ramas neschimbat!")
last_checked = 100
while True:
    minutul = datetime.datetime.now().minute
    if minutul % 10 == 2 and last_checked != minutul:
        reverificaPretul()
        last_checked = minutul
        print("Verific")
