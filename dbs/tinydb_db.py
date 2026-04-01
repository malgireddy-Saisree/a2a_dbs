# dbs/tinydb_db.py

from tinydb import TinyDB, Query

db = TinyDB("tinydb.json")
Product = Query()

# -------------------------------
# INSERT SAMPLE DATA (ONLY ONCE)
# -------------------------------
if len(db) == 0:
    db.insert_multiple([
        {"id": 1, "name": "iPhone 15", "brand": "Apple", "category": "electronics", "price": 1200, "rating": 4.8, "stock": 50},
        {"id": 2, "name": "Samsung Galaxy S23", "brand": "Samsung", "category": "electronics", "price": 1000, "rating": 4.6, "stock": 40},
        {"id": 3, "name": "Dell XPS 13", "brand": "Dell", "category": "electronics", "price": 1500, "rating": 4.7, "stock": 20},
        {"id": 4, "name": "Nike Running Shoes", "brand": "Nike", "category": "fashion", "price": 200, "rating": 4.3, "stock": 100},
        {"id": 5, "name": "Adidas Hoodie", "brand": "Adidas", "category": "fashion", "price": 120, "rating": 4.2, "stock": 70},
        {"id": 6, "name": "Sony Headphones", "brand": "Sony", "category": "electronics", "price": 300, "rating": 4.5, "stock": 60},
        {"id": 7, "name": "Apple MacBook Air", "brand": "Apple", "category": "electronics", "price": 1800, "rating": 4.9, "stock": 15}
    ])


# -------------------------------
# HELPER: find product by name (fuzzy, case-insensitive)
# -------------------------------
def _find_by_name(name_slug: str):
    """
    Match a hyphenated name slug like 'iphone-15' or 'samsung-galaxy-s23'
    against actual product names like 'iPhone 15' or 'Samsung Galaxy S23'.
    Returns the matched product dict or None.
    """
    needle = name_slug.replace("-", " ").lower()
    for product in db.all():
        if product["name"].lower() == needle:
            return product
    # Partial match fallback
    for product in db.all():
        if needle in product["name"].lower():
            return product
    return None


# -------------------------------
# RUN FUNCTION
# -------------------------------
def run(query: str):
    # Preserve original for name extraction, lowercase copy for command matching
    original = query.strip()
    q = original.lower().split()

    if not q:
        return "❌ Empty query"

    command = q[0].upper()

    # ----------------------------
    # GET / SEARCH
    # ----------------------------
    if command == "GET":
        if "all" in q:
            return db.all()
        if "electronics" in q:
            return db.search(Product.category == "electronics")
        if "fashion" in q:
            return db.search(Product.category == "fashion")
        if "apple" in q:
            return db.search(Product.brand == "Apple")
        if "expensive" in q:
            return [p for p in db.all() if p["price"] > 1000]
        if "cheap" in q:
            return [p for p in db.all() if p["price"] < 300]
        return db.all()

    # ----------------------------
    # INSERT
    # INSERT <id> <name-slug> <brand> <category> <price> <rating> <stock>
    # e.g.  INSERT 8 Google-Pixel Google electronics 700 4.3 30
    # ----------------------------
    elif command == "INSERT":
        try:
            parts = original.split()   # keep original casing for name/brand
            new_product = {
                "id":       int(parts[1]),
                "name":     parts[2].replace("-", " "),   # "Google-Pixel" → "Google Pixel"
                "brand":    parts[3],
                "category": parts[4].lower(),
                "price":    int(parts[5]),
                "rating":   float(parts[6]),
                "stock":    int(parts[7])
            }
            db.insert(new_product)
            return f"✅ Product '{new_product['name']}' inserted successfully"
        except Exception as e:
            return f"❌ Invalid INSERT format: {e}"

    # ----------------------------
    # UPDATE — supports BOTH id and name
    # By id:   UPDATE 1 price 1300
    # By name: UPDATE iphone-15 price 1400
    # ----------------------------
    elif command == "UPDATE":
        try:
            parts = original.split()
            identifier = parts[1]           # could be "1" or "iphone-15"
            field      = parts[2].lower()
            value      = parts[3]

            # Cast value to correct type
            if field in ("price", "stock"):
                value = int(value)
            elif field == "rating":
                value = float(value)

            # Numeric id or name slug?
            if identifier.lstrip("-").isdigit():
                product_id = int(identifier)
                matches = db.search(Product.id == product_id)
                if not matches:
                    return f"❌ No product found with id {product_id}"
                db.update({field: value}, Product.id == product_id)
                return f"✅ Product id={product_id} — {field} updated to {value}"
            else:
                product = _find_by_name(identifier)
                if not product:
                    return f"❌ No product found matching '{identifier}'"
                db.update({field: value}, Product.id == product["id"])
                return f"✅ '{product['name']}' — {field} updated to {value}"

        except Exception as e:
            return f"❌ Invalid UPDATE format: {e}"

    # ----------------------------
    # DELETE — supports BOTH id and name
    # By id:   DELETE 1
    # By name: DELETE iphone-15
    # ----------------------------
    elif command == "DELETE":
        try:
            parts = original.split()
            identifier = parts[1]

            if identifier.lstrip("-").isdigit():
                product_id = int(identifier)
                matches = db.search(Product.id == product_id)
                if not matches:
                    return f"❌ No product found with id {product_id}"
                db.remove(Product.id == product_id)
                return f"🗑 Product id={product_id} deleted successfully"
            else:
                product = _find_by_name(identifier)
                if not product:
                    return f"❌ No product found matching '{identifier}'"
                db.remove(Product.id == product["id"])
                return f"🗑 '{product['name']}' deleted successfully"

        except Exception as e:
            return f"❌ Invalid DELETE format: {e}"

    return "❌ Unknown command. Use GET / INSERT / UPDATE / DELETE"


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("📦 ALL PRODUCTS:")
    print(run("GET all"))

    print("\n✏️  UPDATE by NAME (iphone-15 price → 1400):")
    print(run("UPDATE iphone-15 price 1400"))

    print("\n✏️  UPDATE by ID (product 2 rating → 4.9):")
    print(run("UPDATE 2 rating 4.9"))

    print("\n➕ INSERT NEW PRODUCT:")
    print(run("INSERT 8 Google-Pixel Google electronics 700 4.3 30"))

    print("\n🗑 DELETE by NAME:")
    print(run("DELETE google-pixel"))

    print("\n📦 FINAL STATE:")
    print(run("GET all"))


if __name__ == "__main__":
    main()