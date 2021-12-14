import requests
from bs4 import BeautifulSoup
from abc import abstractmethod
import main

class Site():
    @abstractmethod
    def scaneazaPagina(linkulDeMonitorizat):
        pass

class Emag(Site):
    def __init__(self):
        self.numeSite = "Emag"

    def scaneazaPagina(linkulDeMonitorizat):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        html_text = requests.get(linkulDeMonitorizat, headers=headers).text
        print(f"Now Scraping - {linkulDeMonitorizat}")
        soup = BeautifulSoup(html_text, 'html.parser')
        titluProdus = soup.find('h1', {'class': 'page-title'}).get_text().strip()
        print(titluProdus)
        pret = soup.find('p', {'class': 'product-new-price'}).get_text()
        pret = pret.split(" Lei")
        pret = pret[0]
        decimale = pret[-2:]
        pret = pret[:-2]
        pret = pret.replace(".", "")
        pret = pret + "." + decimale
        pret_bun = float(pret)
        print(str(pret_bun))
        return linkulDeMonitorizat, titluProdus, pret_bun

class Altex(Site):
    def __init__(self):
        self.numeSite = "Altex"

    def scaneazaPagina(linkulDeMonitorizat):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        html_text = requests.get(linkulDeMonitorizat, headers=headers).text
        print(f"Now Scraping - {linkulDeMonitorizat}")
        soup = BeautifulSoup(html_text, 'html.parser')
        titluProdus = soup.find('h1', {'class': 'mb-2 font-normal text-2xl md:text-36px leading-32 md:leading-46'}).get_text().strip()
        print(titluProdus)
        pret = soup.find("div", {'class': 'my-2'}).get_text()
        pret = pret.lower()
        pret = pret.split("lei")
        pret = pret[0]
        if "%" in pret:
            pret = pret.split("%")
            pret = pret[1]
        pret = pret.strip()
        pret = pret.replace('.', '')
        # pret = pret.replace(' lei','')
        pret_bun = pret.replace(",",".")
        pret_bun = float(pret_bun)
        print(str(pret_bun))
        return linkulDeMonitorizat, titluProdus, pret_bun


class Flanco(Site):
    def __init__(self):
        self.numeSite = "Flanco"

    def scaneazaPagina(linkulDeMonitorizat):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        html_text = requests.get(linkulDeMonitorizat, headers=headers, allow_redirects=False).text
        print(f"Now Scraping - {linkulDeMonitorizat}")
        soup = BeautifulSoup(html_text, 'html.parser')
        titluProdus = soup.find('h1', {'class': 'page-title'}).get_text().strip()
        print(titluProdus)
        pret = soup.find("div", {'class': 'price-box price-final_price'}).get_text()
        if " lei)" in pret.lower():
            pret = pret.split(" lei)")
            pret = pret[1]
        pret = pret.replace('.','')
        pret = pret.replace(' lei','')
        pret_bun = pret.replace(",",".")
        pret_bun = float(pret_bun)
        print(str(pret_bun))
        return linkulDeMonitorizat, titluProdus, pret_bun

class pretCelMic(Site):
    def __init__(self):
        self.numeSite = "Compari"
    def scaneazaPagina(titlu):
        link_reverifica = "https://www.compari.ro/CategorySearch.php?st=" + str(titlu)
        html_text = requests.get(link_reverifica).text
        soup = BeautifulSoup(html_text, 'html.parser')
        try:
            link_oferte = soup.find('a', {'class': 'offer-num'}).get("href")
        except:
            return None
        if link_oferte:
            html_text_oferte = requests.get(link_oferte).text
            soup = BeautifulSoup(html_text_oferte, 'html.parser')
            lista_produse = soup.findAll("div", {'class': 'optoffer device-desktop'})
            lista_produse_si_preturi = []
            for produs in lista_produse:
                link_produs = produs.find("a", {'class': 'jumplink-overlay initial'}).get("href")
                pret_produs = produs.find("div", {'class': 'row-price'}).get_text()
                pret_produs = pret_produs.strip()
                pret_produs = pret_produs.replace(" RON", "")
                pret_produs = pret_produs.replace(" ", "")
                pret_produs = pret_produs.replace(",", ".")
                pret_produs = float(pret_produs)
                lista_produse_si_preturi.append((link_produs, pret_produs))

            pret_micut = float(9999999999999)
            for pret in lista_produse_si_preturi:
                if pret[1] < pret_micut:
                    pret_micut = pret[1]
                    link_micut = pret[0]

            main.mycursor.execute(f"SELECT pret FROM datesite WHERE titlu_produs='{titlu}'")
            pret_afisaz = main.mycursor.fetchall()
            pret_afisaz = float(pret_afisaz[0][0])
            if pret_afisaz < pret_micut:
                main.mycursor.execute(f"SELECT link FROM datesite WHERE titlu_produs='{titlu}'")
                link_micut2 = main.mycursor.fetchall()
                return pret_afisaz, link_micut2[0][0]
            elif pret_afisaz > pret_micut:
                try:
                    return pret_micut, link_micut
                except:
                    return None
            else:
                main.mycursor.execute(f"SELECT link FROM datesite WHERE titlu_produs='{titlu}'")
                link_micut2 = main.mycursor.fetchall()
                return pret_afisaz, link_micut2[0][0]
        else:
            return None

