import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewelry_shop.settings')
django.setup()

from shop.models import Product

def seed():
    # Clear existing products
    print("Clearing existing products...")
    Product.objects.all().delete()

    products_data = [
        {
            "name": "Rose Gold Classic Necklace",
            "category": "Necklaces",
            "price": 299.00,
            "image_filename": "1-Necklace-RG.webp",
            "description": "An elegant classic rose gold chain necklace, featuring a delicate craftsmanship that makes it perfect for both daily wear and special evening occasions."
        },
        {
            "name": "Aura Diamond Necklace",
            "category": "Necklaces",
            "price": 349.00,
            "image_filename": "neckless2.webp",
            "description": "A sparkling pendant necklace designed with a halo of brilliant crystals that capture the light from every angle, suspended on a fine silver chain."
        },
        {
            "name": "Twin Pendant Necklace Set",
            "category": "Necklaces",
            "price": 499.00,
            "image_filename": "nentwin set.webp",
            "description": "A luxury layered necklace set featuring two beautifully matched pendants that create a sophisticated, modern silhouette."
        },
        {
            "name": "Orbit Sparkle Earrings",
            "category": "Earrings",
            "price": 189.00,
            "image_filename": "orbitsparkle.webp",
            "description": "Unique orbital drop earrings adorned with pave-set zirconia that sway gently with every movement, creating a subtle yet brilliant sparkle."
        },
        {
            "name": "Royal Emerald Pendant",
            "category": "Pendants",
            "price": 220.00,
            "image_filename": "pendal.webp",
            "description": "A stunning vintage-inspired pendant showcasing a rich emerald-cut crystal bordered by a micro-pave silver setting."
        },
        {
            "name": "Teardrop Pearl Pendant",
            "category": "Pendants",
            "price": 240.00,
            "image_filename": "pendal2.webp",
            "description": "A elegant teardrop pendant displaying a single high-lustre freshwater pearl suspended below an intricate gold bale."
        },
        {
            "name": "Minimalist Gold Pendant",
            "category": "Pendants",
            "price": 150.00,
            "image_filename": "pendal3.webp",
            "description": "A modern, geometric flat-disc pendant in polished 18k yellow gold vermeil. A versatile accessory that layers beautifully."
        },
        {
            "name": "Starlight Silver Pendant",
            "category": "Pendants",
            "price": 175.00,
            "image_filename": "pendal4.webp",
            "description": "A whimsical starburst pendant crafted in fine 925 sterling silver, embellished with miniature sparkling gemstones."
        },
        {
            "name": "Solitaire Diamond Ring",
            "category": "Rings",
            "price": 599.00,
            "image_filename": "ring.webp",
            "description": "A classic engagement-style ring with a high-set sparkling solitaire stone on a polished platinum-finished band."
        },
        {
            "name": "Eternal Gold Band",
            "category": "Rings",
            "price": 299.00,
            "image_filename": "ring2.avif",
            "description": "A solid yellow gold band featuring a polished dome profile. An essential, timeless addition to any jewelry stack."
        },
        {
            "name": "Infinity Rose Gold Ring",
            "category": "Rings",
            "price": 349.00,
            "image_filename": "ring3.webp",
            "description": "A beautiful infinity-twist band crafted in 14k rose gold, partially set with delicate sparkling accents for a touch of elegance."
        }
    ]

    print("Seeding products...")
    for prod in products_data:
        inr_price = round(prod["price"] * 83, -2)
        p = Product.objects.create(
            name=prod["name"],
            category=prod["category"],
            price=inr_price,
            image=prod["image_filename"],
            description=prod["description"],
            stock=15
        )
        print(f"Created Product: {p.name} ({p.category}) - Rs. {p.price}")
        
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed()
