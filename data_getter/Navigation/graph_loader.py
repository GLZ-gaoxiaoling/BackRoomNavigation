import sqlite3
import json

def get_graph_from_db(db_path):
    """
    从数据库中获取图的数据结构。
    """
    graph = {}
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM levels_table;")
    rows = cursor.fetchall()
    for row in rows:
        current_node = row[0]
        reachable_nodes = json.loads(row[1])
        graph[current_node] = reachable_nodes
    cursor.close()
    conn.close()
    return graph
