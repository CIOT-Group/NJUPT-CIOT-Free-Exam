import json
from collections import defaultdict, deque


def find_indegree(graph, num_nodes):
    # 初始化入度列表，长度为节点数，每个元素初始值为0
    indegree = [0] * num_nodes
    for u in range(num_nodes):
        # 遍历当前节点的邻接节点及其边权
        for v, _ in graph[u]:
            # 如果邻接节点存在，则将其入度加1
            indegree[v] += 1
    return indegree


def topological_sort(graph, num_nodes):
    # 找到每个节点的入度
    indegree = find_indegree(graph, num_nodes)
    # 找到入度为0的节点
    zero_indegree = deque()
    for i in range(num_nodes):
        if indegree[i] == 0:
            zero_indegree.append(i)

    topo_order = []
    # 遍历入度为0的节点
    while len(zero_indegree) > 0:
        # 取出一个入度为0的节点
        u = zero_indegree.popleft()
        # 添加到拓扑排序的结果中
        topo_order.append(u)
        # 遍历该节点的邻接节点
        for v, _ in graph[u]:
            # 邻接节点的入度减1
            indegree[v] -= 1
            # 如果邻接节点的入度为0，则添加到入度为0的队列中
            if indegree[v] == 0:
                zero_indegree.append(v)

    # 如果拓扑排序的结果长度等于节点数，则返回拓扑排序的结果，否则返回空列表
    if len(topo_order) == num_nodes:
        return topo_order
    else:
        return []


def aoe_network(data):
    events = data['events']
    activities = data['activities']

    num_events = len(events)
    # 定义一个图，使用字典，键为事件，值为该事件能到达的其他事件及耗时
    graph = defaultdict(list)
    # 定义一个字典，键为二元组，值为耗时
    durations = {}

    for activity in activities:
        from_event = activity['from_event']
        to_event = activity['to_event']
        duration = activity['duration']
        # 将起始事件能到达的结束事件及耗时添加到图中
        graph[from_event].append((to_event, duration))
        # 将起始事件和结束事件能组成的二元组及耗时添加到字典中
        durations[(from_event, to_event)] = duration

    # 步骤1：拓扑排序
    topo_order = topological_sort(graph, num_events)

    if not topo_order:
        print("AOE网中存在环, 无法顺利进行")
        return

    # 步骤2：计算最早开始时间
    earliest_start = [0] * num_events
    for u in topo_order:
        for v, duration in graph[u]:
            earliest_start[v] = max(
                earliest_start[v], earliest_start[u] + duration)

    # 步骤3：计算最迟开始时间
    latest_start = [float('inf')] * num_events
    latest_start[topo_order[-1]] = earliest_start[topo_order[-1]]

    for u in reversed(topo_order):
        for v, duration in graph[u]:
            latest_start[u] = min(latest_start[u], latest_start[v] - duration)

    # 步骤4：计算最早发生时间和最迟发生时间
    critical_activities = []
    for activity in activities:
        from_event = activity['from_event']
        to_event = activity['to_event']
        duration = activity['duration']
        Aearly = earliest_start[from_event]
        Alate = latest_start[to_event] - duration

        # 如果最早发生时间和最迟发生时间相等，则该活动为关键活动
        if Aearly == Alate:
            critical_activities.append({
                'name': activity['name'],
                'from_event': from_event,
                'to_event': to_event,
                'earliest_start': Aearly,
                'latest_start': Alate
            })

    # 步骤5：计算最小项目工期
    project_duration = earliest_start[topo_order[-1]]

    print(f"最小项目工期: {project_duration}")
    print("关键活动 | 顶点1 | 顶点2 | 最早发生时间 | 最迟发生时间")
    for ca in critical_activities:
        print(
            f"{ca['name']}\t{ca['from_event']}\t{ca['to_event']}\t{ca['earliest_start']}\t{ca['latest_start']}")


if __name__ == "__main__":
    data = json.load(open("aoe_network.json"))
    aoe_network(data)
