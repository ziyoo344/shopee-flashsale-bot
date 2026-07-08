#!/usr/bin/env python3
"""
Shopee Flash Sale Auto Order Bot
Fitur:
- Auto order produk flash sale
- Load cookies otomatis
- Support multiple keywords
- Support varian produk
- Auto checkout
"""

import os
import sys
import time
import json
from colorama import init, Fore, Style
from core import BrowserManager, AuthManager, OrderManager, Utils

# Inisialisasi colorama
init(autoreset=True)

class ShopeeFlashSaleBot:
    def __init__(self):
        self.browser = BrowserManager(headless=False)
        self.auth = None
        self.order = None
        self.config = self.load_config()
        
    def load_config(self):
        """Load konfigurasi dari file atau default"""
        default_config = {
            'product_keywords': ['iphone', 'samsung', 'xiaomi'],  # Ganti dengan keyword produk yang diinginkan
            'variant': None,  # Contoh: 'Black', '64GB'
            'address': None,  # Contoh: 'Rumah', 'Kantor'
            'payment': 'ShopeePay',  # Metode pembayaran
            'check_interval': 0.5,  # Interval pengecekan dalam detik
            'max_attempts': 5,  # Maksimal percobaan
            'auto_start': False  # Auto start tanpa konfirmasi
        }
        
        # Coba load dari file config
        config_file = 'config.json'
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
                    print(f"{Fore.GREEN}✅ Load konfigurasi dari {config_file}")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Gagal load config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save konfigurasi ke file"""
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"{Fore.GREEN}✅ Konfigurasi disimpan ke config.json")
            return True
        except Exception as e:
            print(f"{Fore.RED}❌ Gagal save config: {e}")
            return False
    
    def display_banner(self):
        """Menampilkan banner bot"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════╗
{Fore.CYAN}║  {Fore.YELLOW}🏪 SHOPEE FLASH SALE AUTO ORDER BOT v1.0        {Fore.CYAN}║
{Fore.CYAN}║  {Fore.GREEN}⚡ Auto order produk flash sale dengan mudah     {Fore.CYAN}║
{Fore.CYAN}║  {Fore.MAGENTA}🔒 Support login & cookies auto load           {Fore.CYAN}║
{Fore.CYAN}╚═══════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def display_menu(self):
        """Menampilkan menu utama"""
        print(f"\n{Fore.CYAN}📋 MENU UTAMA:")
        print(f"{Fore.WHITE}1. {Fore.GREEN}Mulai Auto Order Flash Sale")
        print(f"{Fore.WHITE}2. {Fore.BLUE}Login Manual (untuk mendapatkan cookies)")
        print(f"{Fore.WHITE}3. {Fore.YELLOW}Load Cookies dari file")
        print(f"{Fore.WHITE}4. {Fore.MAGENTA}Konfigurasi")
        print(f"{Fore.WHITE}5. {Fore.RED}Exit")
        
        choice = input(f"\n{Fore.CYAN}Pilih menu (1-5): {Fore.WHITE}")
        return choice
    
    def setup_browser(self):
        """Setup browser"""
        print(f"{Fore.CYAN}🔧 Setup browser...")
        if self.browser.setup_driver():
            print(f"{Fore.GREEN}✅ Browser berhasil diinisialisasi")
            return True
        else:
            print(f"{Fore.RED}❌ Gagal inisialisasi browser")
            return False
    
    def load_cookies_auto(self):
        """Load cookies otomatis"""
        print(f"{Fore.CYAN}🍪 Mengecek cookies...")
        
        cookie_file = 'cookies.json'
        if os.path.exists(cookie_file):
            try:
                # Navigasi ke Shopee dulu sebelum load cookies
                self.browser.navigate_to('https://shopee.co.id/')
                time.sleep(2)
                
                if self.auth.load_cookies(cookie_file):
                    # Refresh setelah load cookies
                    self.browser.driver.refresh()
                    time.sleep(3)
                    
                    # Cek status login
                    if self.auth.check_login_status():
                        print(f"{Fore.GREEN}✅ Berhasil login menggunakan cookies!")
                        return True
                    else:
                        print(f"{Fore.YELLOW}⚠️ Cookies tidak valid, silakan login manual")
                        return False
            except Exception as e:
                print(f"{Fore.RED}❌ Gagal load cookies: {e}")
                return False
        else:
            print(f"{Fore.YELLOW}⚠️ File cookies tidak ditemukan")
            return False
    
    def manual_login(self):
        """Login manual"""
        print(f"\n{Fore.CYAN}🔐 Login Manual Shopee")
        print(f"{Fore.YELLOW}Silakan login secara manual di browser yang terbuka")
        print(f"{Fore.YELLOW}Setelah berhasil login, cookies akan otomatis disimpan")
        
        username = input(f"{Fore.WHITE}Username/Email (optional): {Fore.WHITE}")
        password = input(f"{Fore.WHITE}Password (optional): {Fore.WHITE}")
        
        if self.auth.login_manual(username if username else None, password if password else None):
            print(f"{Fore.GREEN}✅ Login berhasil! Cookies tersimpan.")
            return True
        else:
            print(f"{Fore.RED}❌ Login gagal")
            return False
    
    def configure_settings(self):
        """Konfigurasi pengaturan bot"""
        print(f"\n{Fore.CYAN}⚙️ KONFIGURASI BOT")
        
        # Keyword produk
        print(f"{Fore.WHITE}Masukkan keyword produk (pisahkan dengan koma):")
        print(f"{Fore.YELLOW}Contoh: iphone, samsung, xiaomi")
        keywords = input(f"{Fore.WHITE}Keyword: {Fore.WHITE}")
        if keywords:
            self.config['product_keywords'] = [k.strip() for k in keywords.split(',')]
        
        # Varian
        variant = input(f"{Fore.WHITE}Varian produk (optional, Enter untuk skip): {Fore.WHITE}")
        if variant:
            self.config['variant'] = variant
        
        # Alamat
        address = input(f"{Fore.WHITE}Alamat pengiriman (optional): {Fore.WHITE}")
        if address:
            self.config['address'] = address
        
        # Metode pembayaran
        print(f"{Fore.WHITE}Metode pembayaran:")
        print(f"1. ShopeePay")
        print(f"2. Bank Transfer")
        print(f"3. COD")
        payment_choice = input(f"{Fore.WHITE}Pilih (1-3): {Fore.WHITE}")
        
        payment_map = {
            '1': 'ShopeePay',
            '2': 'Bank Transfer',
            '3': 'COD'
        }
        if payment_choice in payment_map:
            self.config['payment'] = payment_map[payment_choice]
        
        # Interval pengecekan
        interval = input(f"{Fore.WHITE}Interval pengecekan (detik, default 0.5): {Fore.WHITE}")
        if interval:
            try:
                self.config['check_interval'] = float(interval)
            except:
                pass
        
        # Max attempts
        attempts = input(f"{Fore.WHITE}Maksimal percobaan (default 5): {Fore.WHITE}")
        if attempts:
            try:
                self.config['max_attempts'] = int(attempts)
            except:
                pass
        
        self.save_config()
        print(f"{Fore.GREEN}✅ Konfigurasi berhasil disimpan!")
    
    def run_auto_order(self):
        """Menjalankan proses auto order"""
        print(f"\n{Fore.CYAN}🚀 Memulai Auto Order Flash Sale")
        print(f"{Fore.YELLOW}Target produk: {', '.join(self.config['product_keywords'])}")
        print(f"{Fore.YELLOW}Metode pembayaran: {self.config['payment']}")
        
        # Inisialisasi order manager
        self.order = OrderManager(self.browser)
        
        attempts = 0
        success = False
        
        while attempts < self.config['max_attempts'] and not success:
            attempts += 1
            print(f"\n{Fore.CYAN}📌 Percobaan ke-{attempts}")
            
            try:
                # Proses auto order
                result = self.order.auto_order_process(
                    product_keywords=self.config['product_keywords'],
                    variant=self.config['variant'],
                    address=self.config['address'],
                    payment=self.config['payment']
                )
                
                if result:
                    print(f"{Fore.GREEN}✅ Auto order berhasil!")
                    success = True
                    break
                else:
                    print(f"{Fore.YELLOW}⚠️ Auto order gagal, mencoba lagi...")
                    
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}")
            
            # Delay sebelum percobaan berikutnya
            if not success and attempts < self.config['max_attempts']:
                time.sleep(self.config['check_interval'])
        
        if success:
            print(f"\n{Fore.GREEN}🎉 Auto order flash sale BERHASIL!")
            print(f"{Fore.CYAN}Silakan cek pesanan Anda di aplikasi Shopee.")
        else:
            print(f"\n{Fore.RED}❌ Auto order gagal setelah {self.config['max_attempts']} percobaan")
            print(f"{Fore.YELLOW}💡 Tips:")
            print(f"   - Pastikan produk flash sale tersedia")
            print(f"   - Coba refresh halaman manual")
            print(f"   - Periksa koneksi internet")
    
    def main(self):
        """Main function"""
        self.display_banner()
        
        # Setup browser
        if not self.setup_browser():
            return
        
        # Inisialisasi auth
        self.auth = AuthManager(self.browser)
        
        # Navigasi ke Shopee
        self.browser.navigate_to('https://shopee.co.id/')
        time.sleep(2)
        
        # Auto load cookies di awal
        print(f"\n{Fore.CYAN}🍪 Mencoba load cookies otomatis...")
        cookie_loaded = self.load_cookies_auto()
        
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                # Auto order
                if not cookie_loaded:
                    print(f"{Fore.YELLOW}⚠️ Anda belum login. Silakan login terlebih dahulu.")
                    continue
                
                # Konfirmasi sebelum mulai
                print(f"\n{Fore.YELLOW}⚠️ Pastikan:")
                print(f"   - Anda sudah login di Shopee")
                print(f"   - Produk flash sale yang dituju tersedia")
                print(f"   - Metode pembayaran sudah siap")
                
                confirm = input(f"\n{Fore.CYAN}Lanjutkan auto order? (y/n): {Fore.WHITE}")
                if confirm.lower() == 'y':
                    self.run_auto_order()
                else:
                    print(f"{Fore.YELLOW}❌ Dibatalkan")
            
            elif choice == '2':
                # Login manual
                cookie_loaded = self.manual_login()
                
            elif choice == '3':
                # Load cookies
                if self.load_cookies_auto():
                    cookie_loaded = True
            
            elif choice == '4':
                # Konfigurasi
                self.configure_settings()
                
            elif choice == '5':
                # Exit
                print(f"\n{Fore.CYAN}👋 Terima kasih telah menggunakan Shopee Flash Sale Bot!")
                break
            
            else:
                print(f"{Fore.RED}❌ Pilihan tidak valid!")
        
        # Cleanup
        self.browser.close()

def main():
    """Entry point"""
    try:
        bot = ShopeeFlashSaleBot()
        bot.main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⏹️ Bot dihentikan oleh pengguna")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error tidak terduga: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()