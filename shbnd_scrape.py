from colorama import Fore, Style, init
import pyfiglet
import time
import sys
import io
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path  
import undetected_chromedriver as uc
from seleniumbase import Driver
from seleniumwire import webdriver
import sqlite3
from datetime import datetime

date_scraped = datetime.now().strftime("%d-%m-%Y %H:%M:%S")


sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
conn = sqlite3.connect("ilanlar_ev.db")
cursor = conn.cursor()

# ilanlar tablosu: sabit bilgiler
cursor.execute("""
CREATE TABLE IF NOT EXISTS ilanlar (
    ilan_id TEXT PRIMARY KEY,
    title TEXT,
    city TEXT,
    town TEXT,
    ilan_date TEXT
);
""")

# fiyat_takibi tablosu: dinamik bilgiler (deneme amacli)
cursor.execute("""
CREATE TABLE IF NOT EXISTS fiyat_takibi (
    ilan_id TEXT,
    price TEXT,
    date_scraped TEXT,
    FOREIGN KEY (ilan_id) REFERENCES ilanlar(ilan_id)
);
""")

conn.commit()





def print_ascii_art():
    ascii_art = pyfiglet.figlet_format("Pirik3", font="slant")
    print(ascii_art)

print_ascii_art()

# Her Sayfada 50 ürün olduğu için bu sayı 50 ve katları olarak yükselecek
sayfa_numarasi = 0

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
chrome_options.add_argument('--headless')

driver = Driver(uc=True)

while True:
    try:
        if sayfa_numarasi == 0:
            url = "https://www.sahibinden.com/satilik?viewType=List&pagingSize=50"
        else:
            url = f"https://www.sahibinden.com/satilik?viewType=List&pagingOffset={sayfa_numarasi}&pagingSize=50"

        print(f"\n--- Sayfa: {sayfa_numarasi // 50 + 1} ---")
        driver.get(url)
        time.sleep(5)
        
        for i in range(1, 51):
            try:                    
                id_element = driver.find_element(By.XPATH, f"/html/body/div[5]/div[3]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[2]/div[1]")
                ilan_id = id_element.text.strip().lstrip('#')
            except:
                ilan_id = "Veri Yok"
                
            try:
                ilan_title = driver.find_element(
                    By.XPATH, f"/html/body/div[5]/div[3]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[2]/a[1]")
                ilan_title = ilan_title.text
            except:
                ilan_title = "Veri Yok"
                
            try:
                ilan_price = driver.find_element(
                    By.XPATH, f"/html/body/div[5]/div[3]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[3]/div/span")
                ilan_price = ilan_price.text
            except:
                ilan_price = "Veri Yok"
                
            try:
                ilan_date = driver.find_element(
                    By.XPATH, f"/html/body/div[5]/div[3]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[4]/span[1]")
                ilan_date = ilan_date.text
            except:
                ilan_date = "Veri Yok"
                
            try:
                location_text = driver.find_element(
                    By.XPATH, f"/html/body/div[5]/div[3]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[5]"
                ).text
                parts = location_text.split()
                ilan_city = parts[0] if len(parts) > 0 else "Veri Yok"
                ilan_town = parts[1] if len(parts) > 1 else "Veri Yok"
            except:
                ilan_city = "Veri Yok"
                ilan_town = "Veri Yok"
                
            print(f"ID: {ilan_id}, Title: {ilan_title}, Price: {ilan_price}, Date: {ilan_date}, City: {ilan_city}, Town: {ilan_town}")

            # Fiyat değişimi kontrolü
            cursor.execute("SELECT price FROM fiyat_takibi WHERE ilan_id = ? ORDER BY date_scraped DESC LIMIT 1", (ilan_id,))
            son_kayit = cursor.fetchone()
                
            if son_kayit and son_kayit[0] == ilan_price:
                print(f"[~] {ilan_id} fiyatı değişmedi, atlandı.")
            else:
                # ilanlar tablosunda ilan var mı kontrolü
                cursor.execute("SELECT 1 FROM ilanlar WHERE ilan_id = ?", (ilan_id,))
                exists = cursor.fetchone()

                if not exists:
                    # Yeni ilan: hem ilanlar hem fiyat_takibi tablosuna ekle
                    try:
                        cursor.execute("""
                            INSERT INTO ilanlar (ilan_id, title, city, town, ilan_date)
                            VALUES (?, ?, ?, ?, ?)
                        """, (ilan_id, ilan_title, ilan_city, ilan_town, ilan_date))

                        print(f"[+] Yeni ilan eklendi: {ilan_id}")
                    except Exception as e:
                        print(f"[!] ilanlar tablosuna ekleme hatası: {e}")

                # fiyat_takibi tablosuna yeni fiyatı kaydet
                try:
                    cursor.execute("""
                        INSERT INTO fiyat_takibi (ilan_id, price, date_scraped)
                        VALUES (?, ?, ?)
                    """, (ilan_id, ilan_price, date_scraped))
                    conn.commit()
                    print(f"[✓] Fiyat kaydedildi: {ilan_id} - {ilan_price}")
                except Exception as e:
                    print(f"[!] fiyat_takibi hatası: {e}")

        # Next page
        sayfa_numarasi += 50

        if sayfa_numarasi > 950:  # her 50 bir adet sayfa numarasina esit ve her iki 50 ve katlari degerleri arasinda 50 adet sayfa var.
            print("Maksimum sayfa sayısına ulaşıldı.")
            break
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        break
                
