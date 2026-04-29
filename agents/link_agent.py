from config import Config
from utils import Utils

class LinkAgent:
    """Automatic affiliate link generation agent"""
    
    def __init__(self):
        self.platforms = Config.AFFILIATE_PLATFORMS
        self.utils = Utils()
    
    def generate_links(self, product_name):
        """Generate links for all enabled platforms"""
        links = {}
        
        if self.platforms["amazon"]["enabled"]:
            links["amazon"] = self._create_amazon_link(product_name)
        
        if self.platforms["aliexpress"]["enabled"]:
            links["aliexpress"] = self._create_aliexpress_link(product_name)
        
        if self.platforms["clickbank"]["enabled"]:
            links["clickbank"] = self._create_clickbank_link(product_name)
        
        return links
    
    def _create_amazon_link(self, product):
        """Create Amazon affiliate link"""
        tag = self.platforms["amazon"]["tag"]
        long_link = Utils.create_amazon_link(product, tag)
        short_link = Utils.shorten_url(long_link)
        
        return {
            "platform": "Amazon",
            "long_url": long_link,
            "short_url": short_link,
            "commission": "1-10%"
        }
    
    def _create_aliexpress_link(self, product):
        """Create AliExpress link"""
        long_link = Utils.create_aliexpress_link(product)
        short_link = Utils.shorten_url(long_link)
        
        return {
            "platform": "AliExpress",
            "long_url": long_link,
            "short_url": short_link,
            "commission": "5-8%"
        }
    
    def _create_clickbank_link(self, product):
        """Create ClickBank hoplink placeholder"""
        nickname = self.platforms["clickbank"]["nickname"]
        
        return {
            "platform": "ClickBank",
            "long_url": f"https://clickbank.com (search: {product})",
            "short_url": "Manual setup needed",
            "commission": "50-75%",
            "note": "Find product in marketplace first"
        }
    
    def get_best_link(self, product_name):
        """Get highest commission link"""
        links = self.generate_links(product_name)
        
        # Priority: ClickBank > AliExpress > Amazon
        if "clickbank" in links:
            return links["clickbank"]
        elif "aliexpress" in links:
            return links["aliexpress"]
        elif "amazon" in links:
            return links["amazon"]
        
        return None
    
    def add_link_to_pin(self, pin_data, platform="auto"):
        """Add affiliate link to pin"""
        product = pin_data.get("product", "")
        
        if platform == "auto":
            link_data = self.get_best_link(product)
        else:
            links = self.generate_links(product)
            link_data = links.get(platform.lower(), {})
        
        pin_data["affiliate_link"] = link_data.get("short_url", "")
        pin_data["link_platform"] = link_data.get("platform", "")
        pin_data["commission_rate"] = link_data.get("commission", "")
        pin_data["status"] = "ready"
        
        return pin_data
