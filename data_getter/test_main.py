from Navigation.graph_loader import get_graph_from_db
from Navigation.path_finder import bfs_shortest_path

# 从数据库中获取图的数据结构
graph = get_graph_from_db('level_exit.db')

# 测试示例：找到从level11 到level48 的最短路径
shortest_path_to_48 = bfs_shortest_path(graph, '114', '48')
print("欢迎使用后室导航,以下为level11 到level48 的最短路径:")
print(shortest_path_to_48)
