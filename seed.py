import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from rental.models import Category, Machinery

def populate_db():
    print("Seeding database with heavy machinery entries...")

    data = [
        {
            "category": "Bulldozers",
            "cat_desc": "Heavy earthmoving and soil pushing equipment.",
            "machines": [
                {"name": "Caterpillar D4", "hourly": 85.00, "daily": 600.00, "status": "Available"},
                {"name": "Caterpillar D6", "hourly": 120.00, "daily": 900.00, "status": "Available"},
                {"name": "Caterpillar D7", "hourly": 160.00, "daily": 1200.00, "status": "Rented"},
                {"name": "Caterpillar D8", "hourly": 210.00, "daily": 1600.00, "status": "Available"},
            ]
        },
        {
            "category": "Excavators",
            "cat_desc": "Digging, trenching, and material handling machinery.",
            "machines": [
                {"name": "Caterpillar CAT 320", "hourly": 110.00, "daily": 800.00, "status": "Available"},
                {"name": "Komatsu PC200", "hourly": 105.00, "daily": 750.00, "status": "Maintenance"},
            ]
        },
        {
            "category": "Motor Graders",
            "cat_desc": "Road construction and ground leveling equipment.",
            "machines": [
                {"name": "CAT 140G Grader", "hourly": 95.00, "daily": 700.00, "status": "Available"},
            ]
        },
        {
            "category": "Loaders",
            "cat_desc": "Heavy material loading and soil lifting trucks.",
            "machines": [
                {"name": "Wheel Loader 950M", "hourly": 130.00, "daily": 950.00, "status": "Available"},
            ]
        }
    ]

    for item in data:
        cat_obj, _ = Category.objects.get_or_create(
            name=item["category"],
            defaults={"description": item["cat_desc"]}
        )
        for m in item["machines"]:
            Machinery.objects.get_or_create(
                category=cat_obj,
                name=m["name"],
                defaults={
                    "rate_hourly": m["hourly"],
                    "rate_daily": m["daily"],
                    "status": m["status"]
                }
            )

    print(" Database successfully seeded!")

if __name__ == "__main__":
    populate_db()