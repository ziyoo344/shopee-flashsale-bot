import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import random

class BrowserManager:
    def __init__(self, headless=False):
        self.driver = None
        self.wait = None
        self.headless = headless
        self.ua = UserAgent()
        
    def setup_driver(self):
        """Setup Chrome driver dengan konfigurasi optimal"""
        options = Options()
        
        # Konfigurasi dasar
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(f'--user-agent={self.ua.random}')
        
        # Blokir notifikasi dan popup
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        # Optimasi performa
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Headless mode jika diperlukan
        if self.headless:
            options.add_argument('--headless=new')
        
        # Preferensi tambahan
        prefs = {
            'profile.default_content_setting_values': {
                'cookies': 1,
                'images': 1,
                'javascript': 1,
                'notifications': 2,
                'popups': 2,
                'geolocation': 2
            }
        }
        options.add_experimental_option('prefs', prefs)
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)
            return True
        except Exception as e:
            print(f"❌ Gagal setup driver: {e}")
            return False
    
    def get_driver(self):
        return self.driver
    
    def get_wait(self):
        return self.wait
    
    def navigate_to(self, url):
        """Navigasi ke URL tertentu"""
        try:
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))
            return True
        except Exception as e:
            print(f"❌ Gagal navigasi: {e}")
            return False
    
    def wait_for_element(self, by, value, timeout=20):
        """Menunggu elemen muncul"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"❌ Elemen tidak ditemukan: {e}")
            return None
    
    def click_element(self, by, value, timeout=20):
        """Klik elemen dengan tunggu"""
        try:
            element = self.wait_for_element(by, value, timeout)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
                return True
            return False
        except Exception as e:
            print(f"❌ Gagal klik elemen: {e}")
            return False
    
    def type_text(self, by, value, text, timeout=20):
        """Ketik teks pada elemen"""
        try:
            element = self.wait_for_element(by, value, timeout)
            if element:
                element.clear()
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            print(f"❌ Gagal mengetik: {e}")
            return False
    
    def get_text(self, by, value, timeout=20):
        """Mendapatkan teks dari elemen"""
        try:
            element = self.wait_for_element(by, value, timeout)
            if element:
                return element.text
            return None
        except Exception as e:
            print(f"❌ Gagal mengambil teks: {e}")
            return None
    
    def random_sleep(self, min_sec=1, max_sec=3):
        """Sleep random untuk menghindari deteksi"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    def close(self):
        """Tutup browser"""
        if self.driver:
            self.driver.quit()