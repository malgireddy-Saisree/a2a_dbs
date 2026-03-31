# db/tinydb_db.py

from tinydb import TinyDB, Query

db = TinyDB("tinydb.json")
Product = Query()

# -------------------------------
# Insert realistic sample data (only once)
# -------------------------------
if len(db) == 0:
    db.insert_multiple([
        {
            "id": 1,
            "name": "iPhone 15",
            "brand": "Apple",
            "category": "electronics",
            "price": 1200,
            "rating": 4.8,
            "stock": 50
        },
        {
            "id": 2,
            "name": "Samsung Galaxy S23",
            "brand": "Samsung",
            "category": "electronics",
            "price": 1000,
            "rating": 4.6,
            "stock": 40
        },
        {
            "id": 3,
            "name": "Dell XPS 13",
            "brand": "Dell",
            "category": "electronics",
            "price": 1500,
            "rating": 4.7,
            "stock": 20
        },
        {
            "id": 4,
            "name": "Nike Running Shoes",
            "brand": "Nike",
            "category": "fashion",
            "price": 200,
            "rating": 4.3,
            "stock": 100
        },
        {
            "id": 5,
            "name": "Adidas Hoodie",
            "brand": "Adidas",
            "category": "fashion",
            "price": 120,
            "rating": 4.2,
            "stock": 70
        },
        {
            "id": 6,
            "name": "Sony Headphones",
            "brand": "Sony",
            "category": "electronics",
            "price": 300,
            "rating": 4.5,
            "stock": 60
        },
        {
            "id": 7,
            "name": "Apple MacBook Air",
            "brand": "Apple",
            "category": "electronics",
            "price": 1800,
            "rating": 4.9,
            "stock": 15
        }
    ])

# -------------------------------
# Query Function (SMART FILTERING)
# -------------------------------
def run(query: str):
    query = query.lower()

    # All products
    if "all" in query:
        return db.all()

    # Electronics
    if "electronics" in query:
        return db.search(Product.category == "electronics")

    # Fashion
    if "fashion" in query:
        return db.search(Product.category == "fashion")

    # Expensive products
    if "expensive" in query:
        return [p for p in db.all() if p["price"] > 1000]

    # Cheap products
    if "cheap" in query:
        return [p for p in db.all() if p["price"] < 300]

    # Search by brand
    if "apple" in query:
        return db.search(Product.brand == "Apple")

    if "samsung" in query:
        return db.search(Product.brand == "Samsung")

    return db.all()

# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("📦 ALL PRODUCTS:")
    for item in run("all products"):
        print(item)

    print("\n📱 ELECTRONICS:")
    for item in run("electronics"):
        print(item)

    print("\n💸 EXPENSIVE PRODUCTS (>1000):")
    for item in run("expensive"):
        print(item)

    print("\n🍎 APPLE PRODUCTS:")
    for item in run("apple"):
        print(item)

# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()