import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class OrderManager:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.driver = browser_manager.get_driver()
        self.wait = browser_manager.get_wait()
        self.order_status = {
            'pending': False,
            'processing': False,
            'completed': False,
            'failed': False
        }
    
    def open_flashsale_page(self):
        """Buka halaman flash sale"""
        try:
            url = 'https://shopee.co.id/flash-sale'
            self.browser.navigate_to(url)
            time.sleep(3)
            print("✅ Halaman flash sale terbuka")
            return True
        except Exception as e:
            print(f"❌ Gagal buka halaman flash sale: {e}")
            return False
    
    def check_flashsale_items(self, keywords=None):
        """Cek item flash sale berdasarkan keyword"""
        try:
            items = []
            
            # Cari semua item di flash sale
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".shopee-product-card, .flash-sale-item, .item-card")
            
            print(f"🔍 Menemukan {len(product_elements)} produk flash sale")
            
            for element in product_elements:
                try:
                    # Ambil informasi produk
                    name = element.find_element(By.CSS_SELECTOR, 
                        ".product-name, .item-title, .name").text.strip()
                    
                    price = element.find_element(By.CSS_SELECTOR, 
                        ".price, .sale-price, .current-price").text.strip()
                    
                    discount = element.find_element(By.CSS_SELECTOR, 
                        ".discount, .discount-percent").text.strip()
                    
                    stock = element.find_element(By.CSS_SELECTOR, 
                        ".stock, .quantity").text.strip()
                    
                    item_data = {
                        'name': name,
                        'price': price,
                        'discount': discount,
                        'stock': stock,
                        'element': element
                    }
                    
                    # Filter berdasarkan keyword jika ada
                    if keywords:
                        for keyword in keywords:
                            if keyword.lower() in name.lower():
                                items.append(item_data)
                                break
                    else:
                        items.append(item_data)
                        
                except Exception as e:
                    continue
            
            print(f"✅ Menemukan {len(items)} produk yang sesuai")
            return items
            
        except Exception as e:
            print(f"❌ Gagal cek item flash sale: {e}")
            return []
    
    def select_product(self, product_element):
        """Pilih produk dari flash sale"""
        try:
            # Klik produk
            product_element.click()
            time.sleep(random.uniform(1, 3))
            
            # Tunggu halaman produk loading
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 
                ".product-briefing, .product-detail")))
            
            print("✅ Produk berhasil dipilih")
            return True
        except Exception as e:
            print(f"❌ Gagal pilih produk: {e}")
            return False
    
    def select_variant(self, variant_text=None):
        """Pilih varian produk jika ada"""
        try:
            # Cari tombol varian
            variant_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                ".variation-selector, .variant-item, .option-item")
            
            if variant_buttons:
                if variant_text:
                    for btn in variant_buttons:
                        if variant_text.lower() in btn.text.lower():
                            btn.click()
                            time.sleep(0.5)
                            print(f"✅ Varian '{variant_text}' dipilih")
                            return True
                else:
                    # Pilih varian pertama
                    variant_buttons[0].click()
                    time.sleep(0.5)
                    print("✅ Varian pertama dipilih")
                    return True
            else:
                print("ℹ️ Tidak ada varian")
                return True
                
        except Exception as e:
            print(f"⚠️ Gagal pilih varian: {e}")
            return True
    
    def click_buy_now(self):
        """Klik tombol Beli Sekarang"""
        try:
            # Cari tombol beli sekarang
            buy_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Beli Sekarang')]")
            ))
            
            buy_button.click()
            time.sleep(2)
            print("✅ Klik tombol Beli Sekarang")
            return True
        except Exception as e:
            print(f"❌ Gagal klik Beli Sekarang: {e}")
            return False
    
    def confirm_order(self, address=None, payment_method=None):
        """Konfirmasi pesanan"""
        try:
            # Pilih alamat pengiriman
            if address:
                self.select_address(address)
            
            # Pilih metode pembayaran
            if payment_method:
                self.select_payment(payment_method)
            
            # Klik tombol pesan/order
            order_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Pesan') or contains(text(), 'Order')]")
            ))
            
            order_button.click()
            time.sleep(3)
            print("✅ Pesanan berhasil dibuat")
            self.order_status['completed'] = True
            return True
            
        except Exception as e:
            print(f"❌ Gagal konfirmasi pesanan: {e}")
            return False
    
    def select_address(self, address_text):
        """Pilih alamat pengiriman"""
        try:
            # Cari dan pilih alamat
            address_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                ".address-item, .address-card")
            
            for element in address_elements:
                if address_text.lower() in element.text.lower():
                    element.click()
                    time.sleep(1)
                    print(f"✅ Alamat '{address_text}' dipilih")
                    return True
            
            # Jika tidak ditemukan, pilih yang pertama
            if address_elements:
                address_elements[0].click()
                print("✅ Alamat pertama dipilih")
                return True
                
            return False
        except Exception as e:
            print(f"⚠️ Gagal pilih alamat: {e}")
            return False
    
    def select_payment(self, payment_method):
        """Pilih metode pembayaran"""
        try:
            # Cari metode pembayaran
            payment_elements = self.driver.find_elements(By.CSS_SELECTOR,
                ".payment-option, .payment-method")
            
            for element in payment_elements:
                if payment_method.lower() in element.text.lower():
                    element.click()
                    time.sleep(1)
                    print(f"✅ Metode pembayaran '{payment_method}' dipilih")
                    return True
            
            # Jika tidak ditemukan, pilih yang pertama
            if payment_elements:
                payment_elements[0].click()
                print("✅ Metode pembayaran pertama dipilih")
                return True
                
            return False
        except Exception as e:
            print(f"⚠️ Gagal pilih pembayaran: {e}")
            return False
    
    def auto_order_process(self, product_keywords=None, variant=None, address=None, payment=None):
        """Proses auto order lengkap"""
        try:
            print("🚀 Memulai proses auto order flash sale...")
            
            # Buka halaman flash sale
            if not self.open_flashsale_page():
                return False
            
            # Refresh page beberapa kali untuk memastikan loading
            for i in range(3):
                self.driver.refresh()
                time.sleep(2)
            
            # Cek item flash sale
            items = self.check_flashsale_items(product_keywords)
            
            if not items:
                print("❌ Tidak ada produk yang ditemukan")
                return False
            
            # Pilih produk pertama yang tersedia
            selected_item = items[0]
            print(f"🎯 Memilih produk: {selected_item['name']}")
            
            # Klik produk
            if not self.select_product(selected_item['element']):
                return False
            
            # Pilih varian
            if variant:
                self.select_variant(variant)
            else:
                self.select_variant()
            
            # Klik beli sekarang
            if not self.click_buy_now():
                return False
            
            # Konfirmasi pesanan
            if not self.confirm_order(address, payment):
                return False
            
            print("✅ Auto order flash sale berhasil!")
            return True
            
        except Exception as e:
            print(f"❌ Error dalam auto order: {e}")
            self.order_status['failed'] = True
            return False