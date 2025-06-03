from colorama import Fore, Style, init
import pyfiglet
import time
import random
from selenium import webdriver
import os
import sys
import io
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from chromedriver_py import binary_path 
import undetected_chromedriver as uc
from seleniumbase import Driver
from seleniumwire import webdriver
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

driver.get("https://www.sahibinden.com/satilik?viewType=List&pagingSize=50") # kendi bolgenizde veya loglamak istediginiz bolgenin linki.


while True:
    for i in range(1, 51):
        try:
            if i == 50:
                sayfa_numarasi += 50

            ilan_id = driver.find_element(
                By.XPATH, f"/html/body/div[5]/div[3]/form/div[1]/div[3]/table/tbody/tr[{i}]/td[2]/div[1]")
            ilan_id = id.text.strip().lstrip('#')
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
            

       
        print(f"İD: {ilan_city} \nCounty: {ilan_town}")
