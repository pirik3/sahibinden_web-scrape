import time
from selenium import webdriver
from openpyxl import Workbook
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from chromedriver_py import binary_path  # this will get you the path variab
import undetected_chromedriver as uc
from seleniumbase import Driver
from seleniumwire import webdriver

# kütüphaneleri kontrol eder, yoksa yükler
# os.system("pip install selenium")
# os.system("pip install openpyxl")

print("""       



         d8b 888    888               888                                                d88P        d8b         d8b 888       .d8888b.  
         Y8P 888    888               888                                               d88P         Y8P         Y8P 888      d88P  Y88b 
             888    888               888                                              d88P                          888           .d88P 
 .d88b.  888 888888 88888b.  888  888 88888b.       .d8888b .d88b.  88888b.d88b.      d88P  88888b.  888 888d888 888 888  888     8888"  
d88P"88b 888 888    888 "88b 888  888 888 "88b     d88P"   d88""88b 888 "888 "88b    d88P   888 "88b 888 888P"   888 888 .88P      "Y8b. 
888  888 888 888    888  888 888  888 888  888     888     888  888 888  888  888   d88P    888  888 888 888     888 888888K  888    888 
Y88b 888 888 Y88b.  888  888 Y88b 888 888 d88P d8b Y88b.   Y88..88P 888  888  888  d88P     888 d88P 888 888     888 888 "88b Y88b  d88P 
 "Y88888 888  "Y888 888  888  "Y88888 88888P"  Y8P  "Y8888P "Y88P"  888  888  888 d88P      88888P"  888 888     888 888  888  "Y8888P"  
     888                                                                                    888                                          
Y8b d88P                                                                                    888                                          
 "Y88P"                                                                                     888                                                                                                                          

                                                                                                  
""")
time.sleep(3)


# Her Sayfada 50 ürün olduğu için bu sayı 50 ve katları olarak yükselecek
sayfa_numarasi = 0

workbook = Workbook()  # Excel dosyası oluştur

kolon = workbook.active  # Sütun başlıklarını yaz


kolon["A1"] = "İlan Başlığı"
kolon["B1"] = "İlan ID"
kolon["C1"] = "m² (Brüt)"
kolon["D1"] = "Oda Sayısı"
kolon["E1"] = "Fiyat"
kolon["F1"] = "İlan Basligi"
kolon["G1"] = "İlan Tarihi"
kolon["H1"] = "İl / İlçe"

# driver = webdriver.Chrome() # Web tarayıcıyı aç

#chrome_options = webdriver.ChromeOptions()
chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--disable-accelerated-video-decode')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--verbose')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--remote-debugging-port=9222')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--blink-settings=imagesEnabled=false')

proxy_options = {
        'proxy': {
            'no_proxy': 'localhost,127.0.0.1' # excludes
        }  
    }

# initialize the undetected Chrome driver with specified options
#driver = uc.Chrome(use_subprocess=True, options=chrome_options)
driver = Driver(uc=True)
#driver = uc.Chrome(options=chrome_options,seleniumwire_options=proxy_options)
# driver = uc.Chrome(headless=True)
#driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Firefox()
#driver = webdriver.Chrome() # Web tarayıcıyı aç
# driver.get("https://www.sahibinden.com/satilik-daire?pagingSize=50")
driver.get(
    "https://www.sahibinden.com/satilik-daire/izmir-buca-iscievleri-dicle-mah.?pagingSize=50")
# driver.save_screenshot("datacamp.png")
# Bilgileri çek
time.sleep(30)

while True:
    for i in range(1, 51):
        try:
            if i == 50:
                sayfa_numarasi += 50

            # Model bilgisini al
            odasiyisi = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[4]")
            oda = odasiyisi.text
        except:
            oda = "Veri Yok"

        try:
            # İlan Başlığını al
            ilan_basligi = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[2]/a[1]")
            ilan = ilan_basligi.text
        except:
            ilan = "Veri Yok"

        try:
            # İlan ID al
            ilan_id = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]")
            ilan_id = ilan_id.get_attribute("data-id")
            # ilan_id = ilan_id.text
        except:
            ilan_id = "Veri Yok"

        try:
            # Yıl bilgisini al
            m2brut = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[3]")
            m2 = m2brut.text
        except:
            m2 = "Veri Yok"

        try:
            # il/ilçe bilgisini al
            il_ilce_bilgisi_yazi = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[7]")
            il_ilce_bilgisi_yazi = il_ilce_bilgisi_yazi.text
        except:
            # il_ve_ilce = "Veri Yok"
            il_ilce_bilgisi_yazi = "Veri Yok"

        try:
            # İlan tarihi bilgisini al
            # günü al
            ilan_tarihi_bilgisi_gun = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[6]/span[1]")

            ilan_tarihi_gun = ilan_tarihi_bilgisi_gun.text

            # yılı al
            ilan_tarihi_bilgisi_yil = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[6]/span[2]")
            ilan_tarihi_yil = ilan_tarihi_bilgisi_yil.text
            ilan_tarihi_gun_yil = ilan_tarihi_gun+" "+ilan_tarihi_yil

        except:

            ilan_tarihi_gun_yil = "Veri Yok"

        try:
            # Fiyat bilgisini al
            fiyat_bilgisi = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[4]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[5]/div")
            fiyat = fiyat_bilgisi.text
        except:
            fiyat = "Veri Yok"

        print(f"\nİlan Başlığı:{ilan} \nilan_id:{ilan_id} \nM2(brut):{m2} \nOda Sayisi:{oda} \nFiyat:{fiyat} \nİlan Başlığı:{ilan} \nİlan Tarihi:{ilan_tarihi_gun_yil} \nIl_Ilce:{il_ilce_bilgisi_yazi}  \n{'-' * 50}")

        # Verileri excel dosyasına ekle

        kolon.append([ilan, ilan_id, m2, oda, fiyat, ilan,
                     ilan_tarihi_gun_yil, il_ilce_bilgisi_yazi])

    print("Sonraki sayfaya geçiş yapılıyor...")

    try:
        print("Sayfa Numarası :", sayfa_numarasi)
        # driver.get(f"https://www.sahibinden.com/satilik-daire??pagingOffset={sayfa_numarasi}&pagingSize=50")     # Sonraki sayfaya geçiş yap
        driver.get(
            f"https://www.sahibinden.com/satilik-daire/izmir-buca-iscievleri-dicle-mah.?pagingSize=50")

        time.sleep(5)  # Sayfanın yüklenmesi için 5 saniye bekle

    except:

        print("Son sayfaya ulaşıldı.\nExcel dosyasına kaydedildi.")
        # verileri excel dosyasına kaydet
        workbook.save(
            filename="sahibinden-daire-bilgileri-İzmir-Buca-Dicle Mah.xlsx")

        break
