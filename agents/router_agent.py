# agents/router_agent.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import re
from llm import call_llm


def router_agent(state):
    query = state["query"]

    prompt = f"""
You are an intelligent database routing agent. Analyze the user query and route it to the correct database with a valid, executable command.

User Query: "{query}"

---

### AVAILABLE DATABASES & SCHEMAS

**postgres** - SQLite backend
  Tables:
  - users (id INTEGER, name TEXT)
  - orders (id INTEGER, user_id INTEGER, amount INTEGER)
  Commands: Standard SQL
  Examples:
    - Read:   SELECT * FROM users
    - Insert: INSERT INTO users VALUES (5, 'Tulasi')
    - Update: UPDATE users SET name = 'NewName' WHERE id = 1
    - Delete: DELETE FROM users WHERE id = 5

**mongo** - TinyDB backend (products store)
  Fields: id, name, brand, category (electronics/fashion), price, rating, stock
  Known products:
    id=1  iPhone-15          | id=2  Samsung-Galaxy-S23 | id=3  Dell-XPS-13
    id=4  Nike-Running-Shoes | id=5  Adidas-Hoodie       | id=6  Sony-Headphones
    id=7  Apple-MacBook-Air

  Commands:
    Read:    GET all | GET electronics | GET fashion | GET apple | GET expensive | GET cheap
    Insert:  INSERT <next_id> <Name-Slug> <Brand> <category> <price> <rating> <stock>
    Update:  UPDATE <name-slug> <field> <value>
    Delete:  DELETE <name-slug>

  CRITICAL RULES:
    - UPDATE and DELETE MUST use the hyphenated name slug, NOT a numeric id.
    - Slugs are lowercase with hyphens: "iPhone 15" becomes "iphone-15"
    - INSERT uses next available id (next after 7 is 8)
    - INSERT name uses Title-Case-Hyphens: "Sony TV" becomes "Sony-TV"

  Examples:
    - "update price of iphone 15 to 1400"    -> UPDATE iphone-15 price 1400
    - "change stock of sony headphones to 80" -> UPDATE sony-headphones stock 80
    - "update rating of macbook air to 4.8"  -> UPDATE apple-macbook-air rating 4.8
    - "delete samsung galaxy s23"            -> DELETE samsung-galaxy-s23
    - "add a Sony TV priced 800"             -> INSERT 8 Sony-TV Sony electronics 800 4.4 25

**redis** - In-memory key-value cache
  Commands:
    Read:   GET <key>
    Write:  SET <key> <value>
    Delete: DELETE <key>
    Count:  INCR <key>
    All:    ALL
  Key patterns: session:<id>, token:user:<id>, cache:<page>, rate_limit:user:<id>
  Examples:
    - "add session for user 5": SET session:user5 active
    - "delete session abc123":  DELETE session:abc123

**neo4j** - NetworkX graph (friendships)
  Commands (NO Cypher - use ONLY these exact formats):
    - friends of <name>
    - add friendship <Name1> <Name2>
    - remove friendship <Name1> <Name2>
    - mutual friends <Name1> <Name2>
    - suggest friends for <name>
    - all
  Examples:
    - "add Bob as Alice's friend":      add friendship Alice Bob
    - "remove Sai and John friendship": remove friendship Sai John

---

### RULES
1. Pick the database that owns the data type in the query.
2. Generate a VALID, EXECUTABLE command - never a plain description.
3. For mongo INSERT, infer missing fields with sensible defaults (rating 4.0, stock 10).
4. Return ONLY raw JSON with no markdown, no backticks, no extra text.

### OUTPUT FORMAT
{{
  "db_choice": "postgres|mongo|redis|neo4j",
  "action": "read|add|update|delete",
  "db_query": "<exact executable command>",
  "reason": "<one line explanation>"
}}
"""

    response = call_llm(prompt)
    print("\n🔍 RAW LLM RESPONSE:\n", response)

    cleaned = re.sub(r"```json|```", "", response).strip().strip("`").strip()
    print("\n🧹 CLEANED RESPONSE:\n", cleaned)

    try:
        parsed = json.loads(cleaned)
    except Exception:
        print("❌ JSON PARSE ERROR — Response was:", cleaned)
        raise ValueError("❌ LLM returned invalid JSON")

    print("\n🧠 Parsed Decision:", parsed)

    return {
        **state,
        "user_query": query,
        "db_choice": parsed.get("db_choice"),
        "action": parsed.get("action"),
        "db_query": parsed.get("db_query")
    }


# -------------------------------
# TEST
# -------------------------------
if __name__ == "__main__":
    tests = [
        "update the price of iphone 15 to 1400",
        "delete samsung galaxy s23",
        "update stock of sony headphones to 80",
        "add a Google Pixel priced at 700",
        "Add a new user named Tulasi with id 5",
        "Remove friendship between Sai and John",
        "Delete redis session abc123",
        "Show all products",
    ]
    for t in tests:
        print(f"\n{'='*50}\nQuery: {t}")
        result = router_agent({"query": t})
        print(f"DB: {result['db_choice']} | Action: {result['action']} | Query: {result['db_query']}")