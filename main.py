# main.py

from graph.langgraph_builder import build_graph

graph = build_graph()

def run_query(query):
    result = graph.invoke({
        "query": query,
        "db_choice": None,
        "action": None,
        "db_query": None,
        "db_result": None,
        "final_answer": None
    })
    return result["final_answer"]


if __name__ == "__main__":
    while True:
        q = input("\n💬 Ask: ")
        if q.lower() == "exit":
            break

        print(run_query(q))