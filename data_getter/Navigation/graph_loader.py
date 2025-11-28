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

def get_level_info_from_db(db_path):
    """
    从数据库中获取所有楼层的详细信息。
    """
    level_info = {}
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM level_info;")
        rows = cursor.fetchall()
        for row in rows:
            level_id = row[0]
            level_info[level_id] = {
                'description': row[1],
                'difficulty': row[2]
            }
    except sqlite3.OperationalError:
        # 如果表不存在，返回空字典
        pass
    finally:
        cursor.close()
        conn.close()
    return level_info

def get_combined_data(db_path):
    """
    从数据库中获取图数据和楼层信息的组合。
    """
    graph = get_graph_from_db(db_path)
    level_info = get_level_info_from_db(db_path)
    return graph, level_info
