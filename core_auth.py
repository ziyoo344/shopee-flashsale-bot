import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .browser import BrowserManager

class AuthManager:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.driver = browser_manager.get_driver()
        self.wait = browser_manager.get_wait()
    
    def load_cookies(self, cookie_file='cookies.json'):
        """Load cookies dari file"""
        try:
            if os.path.exists(cookie_file):
                with open(cookie_file, 'r') as f:
                    cookies = json.load(f)
                
                for cookie in cookies:
                    # Hapus key yang tidak diperlukan
                    cookie.pop('domain', None)
                    cookie.pop('sameSite', None)
                    cookie.pop('storeId', None)
                    
                    try:
                        self.driver.add_cookie(cookie)
                    except Exception as e:
                        print(f"⚠️ Gagal add cookie: {e}")
                
                print(f"✅ Berhasil load {len(cookies)} cookies")
                return True
            else:
                print(f"❌ File cookie tidak ditemukan: {cookie_file}")
                return False
        except Exception as e:
            print(f"❌ Gagal load cookies: {e}")
            return False
    
    def save_cookies(self, cookie_file='cookies.json'):
        """Save cookies ke file"""
        try:
            cookies = self.driver.get_cookies()
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f"✅ Berhasil save {len(cookies)} cookies ke {cookie_file}")
            return True
        except Exception as e:
            print(f"❌ Gagal save cookies: {e}")
            return False
    
    def login_manual(self, username=None, password=None):
        """Login manual ke Shopee"""
        try:
            print("🔐 Memulai proses login manual...")
            
            # Buka halaman login
            self.browser.navigate_to('https://shopee.co.id/buyer/login')
            time.sleep(3)
            
            # Pilih login dengan email/phone
            if self.browser.click_element(By.XPATH, "//button[contains(text(), 'Email atau Nomor Ponsel')]"):
                print("✅ Memilih metode login email/phone")
            
            # Input username/email
            if username:
                self.browser.type_text(By.ID, "loginEmail", username)
                print("✅ Mengisi username/email")
            
            # Input password
            if password:
                self.browser.type_text(By.ID, "loginPassword", password)
                print("✅ Mengisi password")
            
            # Klik tombol login
            if self.browser.click_element(By.XPATH, "//button[contains(@class, 'login')]"):
                print("✅ Klik tombol login")
            
            # Tunggu login selesai
            time.sleep(5)
            
            # Cek apakah login berhasil
            if 'shopee' in self.driver.current_url and 'login' not in self.driver.current_url:
                print("✅ Login berhasil!")
                self.save_cookies()
                return True
            else:
                print("❌ Login gagal, silakan coba manual")
                return False
                
        except Exception as e:
            print(f"❌ Error saat login: {e}")
            return False
    
    def check_login_status(self):
        """Cek status login"""
        try:
            # Cek apakah ada elemen yang menandakan sudah login
            elements = self.driver.find_elements(By.CSS_SELECTOR, ".shopee-avatar, .user-avatar")
            if elements:
                print("✅ Status: Sudah login")
                return True
            else:
                print("❌ Status: Belum login")
                return False
        except:
            return False