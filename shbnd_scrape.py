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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
conn = sqlite3.connect("ilanlar_ev.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS ilanlar (
    ilan_id TEXT PRIMARY KEY,
    title TEXT,
    price TEXT,
    date TEXT,
    city TEXT,
    town TEXT
)
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

                
            # database ye ekle
            if ilan_id != "Veri Yok":
                try:
                    cursor.execute("""
                    INSERT OR IGNORE INTO ilanlar (ilan_id, title, price, date, city, town)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (ilan_id, ilan_title, ilan_price, ilan_date, ilan_city, ilan_town))
                    conn.commit()
                    print(f"[good] {ilan_id} kaydedildi.")
                except Exception as e:
                    print(f"[bad] hata: {e}")

        # Next page
        sayfa_numarasi += 50

        if sayfa_numarasi > 2500:  # 50 pages max
            print("Maksimum sayfa sayısına ulaşıldı.")
            break
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        break
                
