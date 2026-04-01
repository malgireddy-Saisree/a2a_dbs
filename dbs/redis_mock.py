# dbs/redis_mock.py

import os
import pickle

# -------------------------------
# FILE TO STORE DATA
# -------------------------------
FILE = "redis_cache.pkl"

# -------------------------------
# LOAD OR CREATE CACHE
# -------------------------------
if os.path.exists(FILE):
    with open(FILE, "rb") as f:
        cache = pickle.load(f)
else:
    cache = {
        "session:abc123": {"user_id": 1, "name": "Sai", "status": "active"},
        "session:def456": {"user_id": 2, "name": "John", "status": "inactive"},
        
        "token:user:1": "token_abc_xyz",
        "token:user:2": "token_def_xyz",

        "cache:homepage": {"visits": 1200, "last_updated": "2026-03-31"},
        
        "rate_limit:user:1": 5,
        "rate_limit:user:2": 2
    }

    # Save initial data
    with open(FILE, "wb") as f:
        pickle.dump(cache, f)


# -------------------------------
# SAVE FUNCTION
# -------------------------------
def save_cache():
    with open(FILE, "wb") as f:
        pickle.dump(cache, f)


# -------------------------------
# Redis-like Operations
# -------------------------------
def run(query: str):
    parts = query.strip().split()

    if not parts:
        return "❌ Empty query"

    command = parts[0].upper()

    # -------------------------------
    # GET
    # -------------------------------
    if command == "GET":
        key = parts[1]
        return cache.get(key, "❌ Key Not Found")

    # -------------------------------
    # SET
    # -------------------------------
    elif command == "SET":
        key = parts[1]
        value = " ".join(parts[2:])
        cache[key] = value
        save_cache()  # 🔥 SAVE
        return f"✅ Set {key}"

    # -------------------------------
    # DELETE
    # -------------------------------
    elif command == "DELETE":
        key = parts[1]
        if key in cache:
            del cache[key]
            save_cache()  # 🔥 SAVE
            return f"🗑 Deleted {key}"
        return "❌ Key Not Found"

    # -------------------------------
    # INCR (counter use case)
    # -------------------------------
    elif command == "INCR":
        key = parts[1]
        cache[key] = int(cache.get(key, 0)) + 1
        save_cache()  # 🔥 SAVE
        return cache[key]

    # -------------------------------
    # SHOW ALL (debug)
    # -------------------------------
    elif command == "ALL":
        return cache

    return "❌ Invalid command"


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("📦 ALL DATA:")
    print(run("ALL"))

    print("\n➕ SET NEW KEY:")
    print(run("SET session:xyz999 {user_id:3,name:Alice}"))

    print("\n📦 AFTER SET:")
    print(run("GET session:xyz999"))

    print("\n📈 INCREMENT RATE LIMIT:")
    print(run("INCR rate_limit:user:1"))

    print("\n🗑 DELETE KEY:")
    print(run("DELETE session:xyz999"))

    print("\n📦 FINAL STATE:")
    print(run("ALL"))


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()