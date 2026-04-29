import os
from datetime import datetime

class Config:
    """Main configuration file"""
    
    # App Settings
    APP_NAME = "Pinterest Automation Hub"
    VERSION = "1.0.0"
    
    # Niches - Add more anytime
    NICHES = {
        "tech": {
            "name": "Technology",
            "keywords": ["gadgets", "electronics", "tech", "smart devices"],
            "products": [
                "wireless earbuds",
                "smart watch", 
                "phone accessories",
                "power bank",
                "bluetooth speaker",
                "USB cable"
            ]
        },
        "health": {
            "name": "Health & Fitness",
            "keywords": ["fitness", "health", "wellness", "workout"],
            "products": [
                "yoga mat",
                "resistance bands",
                "protein powder",
                "fitness tracker",
                "water bottle",
                "dumbbells"
            ]
        },
        "beauty": {
            "name": "Beauty",
            "keywords": ["makeup", "skincare", "beauty", "cosmetics"],
            "products": [
                "makeup brushes",
                "face serum",
                "nail kit",
                "hair dryer",
                "cosmetic bag",
                "eyelash curler"
            ]
        },
        "home": {
            "name": "Home & Kitchen",
            "keywords": ["home", "kitchen", "decor", "organization"],
            "products": [
                "led lights",
                "storage boxes",
                "wall art",
                "coffee maker",
                "organizer",
                "plant pots"
            ]
        },
        "fashion": {
            "name": "Fashion",
            "keywords": ["fashion", "style", "accessories", "clothing"],
            "products": [
                "sunglasses",
                "watch",
                "backpack",
                "wallet",
                "belt",
                "jewelry"
            ]
        }
    }
    
    # Affiliate Settings
    AFFILIATE_PLATFORMS = {
        "amazon": {
            "enabled": True,
            "tag": "yourname-20",  # CHANGE THIS
            "base_url": "https://www.amazon.com"
        },
        "clickbank": {
            "enabled": True,
            "nickname": "yourname",  # CHANGE THIS
            "base_url": "https://clickbank.com"
        },
        "aliexpress": {
            "enabled": True,
            "base_url": "https://www.aliexpress.com"
        }
    }
    
    # Agent Settings
    AGENT_CONFIG = {
        "max_pins_per_batch": 10,
        "default_niche": "tech",
        "auto_link_generation": True,
        "auto_save": True,
        "save_directory": "generated_pins"
    }
    
    # Pin Templates
    PIN_TEMPLATES = {
        "viral": {
            "title": "🔥 {product} - You Won't Believe This!",
            "desc": "Discover the secret to {benefit}! ✨ {product} is trending for a reason. Limited time offer - Click now! 👇",
            "cta": "👉 Click link to check price!"
        },
        "professional": {
            "title": "✅ Best {product} - Expert Recommended",
            "desc": "Professional-grade {product} for {benefit}. Trusted by thousands. Premium quality guaranteed. Get yours today!",
            "cta": "🔗 Shop now - Limited stock!"
        },
        "urgency": {
            "title": "⏰ HURRY! {product} - Limited Stock!",
            "desc": "Don't miss out on {product}! 🚨 Flash sale ending soon. {benefit} guaranteed. Thousands already ordered!",
            "cta": "⚡ Grab yours before it's gone!"
        }
    }

    @staticmethod
    def get_niche_products(niche):
        """Get products for a specific niche"""
        return Config.NICHES.get(niche, {}).get("products", [])
    
    @staticmethod
    def get_all_niches():
        """Get list of all available niches"""
        return list(Config.NICHES.keys())
