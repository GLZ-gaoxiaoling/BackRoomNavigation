from collections import deque


def bfs_shortest_path(graph, start, goal):
    """
    使用广度优先搜索算法找到最短路径。
    """
    # 队列用于存储将要访问的节点
    queue = deque([[start]])

    # 访问过的节点集合
    visited = set()

    while queue:
        # 获取当前路径和当前节点
        path = queue.popleft()
        current_node = path[-1]

        # 如果当前节点是目标节点，返回路径
        if current_node == goal:
            return path

        # 将当前节点添加到访问过的节点集合中
        visited.add(current_node)

        # 将当前节点的邻居节点添加到队列中
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                visited.add(neighbor)

    return None


# PS 全是BUG，不做了，反正也没用
# def dfs_longest_path_to_level_optimized(graph, start, level):
#     """
#     优化后的深度优先搜索算法，用于找到到达指定层级的最长路径。
#     """
#     max_path = []
#     visited = set()
#
#     def dfs(current_node, current_path, current_level):
#         # 如果当前层级等于指定层级，更新最长路径
#         if current_level == level:
#             if len(current_path) > len(max_path):
#                 max_path.clear()
#                 max_path.extend(current_path)
#             return
#
#         # 如果当前路径长度加上剩余可能的最大长度仍然小于当前已知的最长路径长度，则剪枝
#         if len(current_path) + (level - current_level) < len(max_path):
#             return
#
#         # 访问当前节点的邻居
#         for neighbor in graph.get(current_node, []):
#             if neighbor not in visited:
#                 visited.add(neighbor)
#                 dfs(neighbor, current_path + [neighbor], current_level + 1)
#                 visited.remove(neighbor)
#
#     visited.add(start)
#     dfs(start, [start], 1)
#     return max_path
