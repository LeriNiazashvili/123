"""
გაშვება პროექტის root-იდან (სადაც manage.py-ია):
    python manage.py shell < store/seed.py
"""
from store.models import Category, Product


tech, _ = Category.objects.get_or_create(name="ტექნიკა")
clothes, _ = Category.objects.get_or_create(name="ტანსაცმელი")
books, _ = Category.objects.get_or_create(name="წიგნები")


products_data = [
    {"name": "iPhone 15", "price": 2500, "category": tech, "is_discounted": True},
    {"name": "Samsung Galaxy S24", "price": 2300, "category": tech, "is_discounted": False},
    {"name": "MacBook Air M2", "price": 3200, "category": tech, "is_discounted": True},
    {"name": "Sony Headphones", "price": 450, "category": tech, "is_discounted": False},
    {"name": "ჰუდი (Hoodie)", "price": 120, "category": clothes, "is_discounted": True},
    {"name": "ჯინსის შარვალი", "price": 90, "category": clothes, "is_discounted": False},
    {"name": "სპორტული ფეხსაცმელი", "price": 210, "category": clothes, "is_discounted": True},
    {"name": "Django-ს სახელმძღვანელო", "price": 45, "category": books, "is_discounted": False},
    {"name": "Python პროგრამირება", "price": 50, "category": books, "is_discounted": True},
    {"name": "ალგორითმების საფუძვლები", "price": 65, "category": books, "is_discounted": False},
]


for prod in products_data:
    Product.objects.get_or_create(
        name=prod["name"],
        defaults={
            "price": prod["price"],
            "category": prod["category"],
            "is_discounted": prod["is_discounted"]
        }
    )

print("✅ 10 ტესტური პროდუქტი წარმატებით დაემატა ბაზაში!")