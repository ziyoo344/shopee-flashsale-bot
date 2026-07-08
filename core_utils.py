import time
import random
import json
import os
from datetime import datetime

class Utils:
    @staticmethod
    def random_delay(min_sec=0.5, max_sec=2):
        """Delay random"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    @staticmethod
    def get_timestamp():
        """Mendapatkan timestamp sekarang"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def log_message(message, level="INFO"):
        """Log message dengan timestamp"""
        timestamp = Utils.get_timestamp()
        print(f"[{timestamp}] [{level}] {message}")
    
    @staticmethod
    def save_to_file(data, filename):
        """Save data ke file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Gagal save file: {e}")
            return False
    
    @staticmethod
    def load_from_file(filename):
        """Load data dari file"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"❌ Gagal load file: {e}")
            return None