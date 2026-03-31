# db/graph_db.py

import networkx as nx

G = nx.Graph()

# -------------------------------
# Add realistic sample data
# -------------------------------
users = ["Sai", "John", "Alice", "Bob", "Charlie", "David"]

G.add_nodes_from(users)

# Friend relationships
G.add_edges_from([
    ("Sai", "John"),
    ("Sai", "Alice"),
    ("John", "Alice"),
    ("John", "Bob"),
    ("Alice", "Charlie"),
    ("Bob", "David")
])

# -------------------------------
# Graph Operations
# -------------------------------
def run(query: str):
    query = query.lower().strip()

    # -------------------------------
    # GET FRIENDS
    # -------------------------------
    if query.startswith("friends of"):
        name = query.replace("friends of ", "").capitalize()
        if name in G:
            return list(G.neighbors(name))
        return "❌ User not found"

    # -------------------------------
    # MUTUAL FRIENDS
    # -------------------------------
    if query.startswith("mutual friends"):
        parts = query.split()
        if len(parts) >= 4:
            user1 = parts[2].capitalize()
            user2 = parts[3].capitalize()

            if user1 in G and user2 in G:
                mutual = list(nx.common_neighbors(G, user1, user2))
                return mutual
        return "❌ Invalid users"

    # -------------------------------
    # FRIEND SUGGESTIONS
    # -------------------------------
    if query.startswith("suggest friends for"):
        name = query.replace("suggest friends for ", "").capitalize()

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
    if query.startswith("add friendship"):
        parts = query.split()
        if len(parts) >= 4:
            u1 = parts[2].capitalize()
            u2 = parts[3].capitalize()

            G.add_edge(u1, u2)
            return f"✅ Added friendship between {u1} and {u2}"

        return "❌ Invalid command"

    # -------------------------------
    # REMOVE FRIENDSHIP
    # -------------------------------
    if query.startswith("remove friendship"):
        parts = query.split()
        if len(parts) >= 4:
            u1 = parts[2].capitalize()
            u2 = parts[3].capitalize()

            if G.has_edge(u1, u2):
                G.remove_edge(u1, u2)
                return f"🗑 Removed friendship between {u1} and {u2}"

        return "❌ Invalid command"

    # -------------------------------
    # SHOW ALL CONNECTIONS
    # -------------------------------
    if query == "all":
        return list(G.edges())

    return "❌ Unknown query"


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("👥 ALL CONNECTIONS:")
    print(run("all"))

    print("\n🤝 FRIENDS OF Sai:")
    print(run("friends of Sai"))

    print("\n🔗 MUTUAL FRIENDS (Sai & John):")
    print(run("mutual friends Sai John"))

    print("\n💡 FRIEND SUGGESTIONS FOR Sai:")
    print(run("suggest friends for Sai"))

    print("\n➕ ADD FRIENDSHIP:")
    print(run("add friendship Sai David"))

    print("\n👥 UPDATED FRIENDS OF Sai:")
    print(run("friends of Sai"))

    print("\n🗑 REMOVE FRIENDSHIP:")
    print(run("remove friendship Sai David"))

    print("\n👥 FINAL CONNECTIONS:")
    print(run("all"))


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()