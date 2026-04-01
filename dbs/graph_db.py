# dbs/graph_db.py

import os
import pickle
import networkx as nx

# -------------------------------
# FILE TO STORE GRAPH
# -------------------------------
FILE = "graph.pkl"

# -------------------------------
# LOAD OR CREATE GRAPH
# -------------------------------
if os.path.exists(FILE):
    with open(FILE, "rb") as f:
        G = pickle.load(f)
else:
    G = nx.Graph()

    # Initial data
    users = ["Sai", "John", "Alice", "Bob", "Charlie", "David"]
    G.add_nodes_from(users)

    G.add_edges_from([
        ("Sai", "John"),
        ("Sai", "Alice"),
        ("John", "Alice"),
        ("John", "Bob"),
        ("Alice", "Charlie"),
        ("Bob", "David")
    ])

    # Save initial graph
    with open(FILE, "wb") as f:
        pickle.dump(G, f)


# -------------------------------
# SAVE FUNCTION (REUSABLE)
# -------------------------------
def save_graph():
    with open(FILE, "wb") as f:
        pickle.dump(G, f)


# -------------------------------
# GRAPH OPERATIONS
# -------------------------------
def run(query: str):
    query = query.strip()

    # Normalize lowercase only for matching keywords
    q_lower = query.lower()

    # -------------------------------
    # GET FRIENDS
    # -------------------------------
    if q_lower.startswith("friends of"):
        name = query.replace("friends of", "").strip().title()

        if name in G:
            return list(G.neighbors(name))
        return "❌ User not found"

    # -------------------------------
    # MUTUAL FRIENDS
    # -------------------------------
    if q_lower.startswith("mutual friends"):
        parts = query.split()

        if len(parts) >= 4:
            user1 = parts[2].title()
            user2 = parts[3].title()

            if user1 in G and user2 in G:
                return list(nx.common_neighbors(G, user1, user2))

        return "❌ Invalid users"

    # -------------------------------
    # FRIEND SUGGESTIONS
    # -------------------------------
    if q_lower.startswith("suggest friends for"):
        name = query.replace("suggest friends for", "").strip().title()

        if name in G:
            friends = set(G.neighbors(name))
            suggestions = set()

            for friend in friends:
                suggestions.update(G.neighbors(friend))

            suggestions -= friends
            suggestions.discard(name)

            return list(suggestions)

        return "❌ User not found"

    # -------------------------------
    # ADD FRIENDSHIP
    # -------------------------------
    if q_lower.startswith("add friendship"):
        parts = query.split()

        if len(parts) >= 4:
            u1 = parts[2].title()
            u2 = parts[3].title()

            G.add_edge(u1, u2)
            save_graph()  # 🔥 SAVE

            return f"✅ Added friendship between {u1} and {u2}"

        return "❌ Invalid command"

    # -------------------------------
    # REMOVE FRIENDSHIP
    # -------------------------------
    if q_lower.startswith("remove friendship"):
        parts = query.split()

        if len(parts) >= 4:
            u1 = parts[2].title()
            u2 = parts[3].title()

            if G.has_edge(u1, u2):
                G.remove_edge(u1, u2)
                save_graph()  # 🔥 SAVE

                return f"🗑 Removed friendship between {u1} and {u2}"

        return "❌ Invalid command"

    # -------------------------------
    # SHOW ALL CONNECTIONS
    # -------------------------------
    if q_lower == "all":
        return list(G.edges())

    return "❌ Unknown query"


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("👥 ALL CONNECTIONS:")
    print(run("all"))

    print("\n➕ ADD FRIENDSHIP (Sai Tulasi):")
    print(run("add friendship Sai Tulasi"))

    print("\n👥 UPDATED FRIENDS OF Sai:")
    print(run("friends of Sai"))

    print("\n🗑 REMOVE FRIENDSHIP:")
    print(run("remove friendship Sai Tulasi"))

    print("\n👥 FINAL CONNECTIONS:")
    print(run("all"))


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()