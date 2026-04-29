import random
from datetime import datetime
from config import Config

class PinterestAgent:
    """Main Pinterest automation agent"""
    
    def __init__(self):
        self.config = Config()
        self.generated_pins = []
    
    def select_products(self, niche, count=3):
        """Select random products from niche"""
        products = Config.get_niche_products(niche)
        if not products:
            return []
        
        selected = random.sample(products, min(count, len(products)))
        return [{"name": p, "niche": niche} for p in selected]
    
    def create_pin_data(self, product, template_type="viral"):
        """Create complete pin data"""
        template = Config.PIN_TEMPLATES.get(template_type, Config.PIN_TEMPLATES["viral"])
        
        product_name = product["name"].title()
        niche = product["niche"]
        
        # Generate benefit based on niche
        benefits = {
            "tech": "amazing tech experience",
            "health": "better health & fitness",
            "beauty": "glowing skin & beauty",
            "home": "organized beautiful home",
            "fashion": "stunning style & confidence"
        }
        benefit = benefits.get(niche, "better lifestyle")
        
        # Create pin content
        title = template["title"].format(product=product_name)
        description = template["desc"].format(product=product_name, benefit=benefit)
        cta = template["cta"]
        
        # Keywords
        niche_keywords = Config.NICHES[niche]["keywords"]
        keywords = f"{product['name']}, " + ", ".join(niche_keywords) + ", trending, best deals, discount"
        
        return {
            "product": product_name,
            "niche": niche,
            "title": title,
            "description": description,
            "cta": cta,
            "keywords": keywords,
            "template": template_type,
            "created_at": datetime.now().isoformat(),
            "status": "draft"
        }
    
    def generate_batch(self, niche, count=3, template="viral"):
        """Generate multiple pins"""
        products = self.select_products(niche, count)
        pins = []
        
        for product in products:
            pin = self.create_pin_data(product, template)
            pins.append(pin)
        
        self.generated_pins.extend(pins)
        return pins
    
    def get_stats(self):
        """Get generation statistics"""
        return {
            "total_pins": len(self.generated_pins),
            "by_niche": self._count_by_niche(),
            "by_status": self._count_by_status()
        }
    
    def _count_by_niche(self):
        """Count pins by niche"""
        counts = {}
        for pin in self.generated_pins:
            niche = pin.get("niche", "unknown")
            counts[niche] = counts.get(niche, 0) + 1
        return counts
    
    def _count_by_status(self):
        """Count pins by status"""
        counts = {}
        for pin in self.generated_pins:
            status = pin.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts
