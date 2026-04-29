import json
import os
from datetime import datetime
from urllib.parse import quote
import requests

class Utils:
    """Helper functions"""
    
    @staticmethod
    def shorten_url(long_url):
        """Shorten URL using TinyURL"""
        try:
            api_url = f"http://tinyurl.com/api-create.php?url={quote(long_url)}"
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                return response.text
            return long_url
        except:
            return long_url
    
    @staticmethod
    def save_to_json(data, filename):
        """Save data to JSON file"""
        try:
            os.makedirs('generated_pins', exist_ok=True)
            filepath = f"generated_pins/{filename}"
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except:
            return False
    
    @staticmethod
    def load_from_json(filename):
        """Load data from JSON file"""
        try:
            filepath = f"generated_pins/{filename}"
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    def format_timestamp():
        """Get formatted timestamp"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def create_amazon_link(product_name, tag):
        """Create Amazon affiliate link"""
        search_query = quote(product_name)
        return f"https://www.amazon.com/s?k={search_query}&tag={tag}"
    
    @staticmethod
    def create_aliexpress_link(product_name):
        """Create AliExpress link"""
        search_query = quote(product_name)
        return f"https://www.aliexpress.com/wholesale?SearchText={search_query}"
