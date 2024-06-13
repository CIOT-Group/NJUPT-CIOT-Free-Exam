import networkx as nx
import matplotlib.pyplot as plt
import json


def draw_aoe_network(data):
    # 创建有向图
    G = nx.DiGraph()

    # 添加事件节点
    for event in data["events"]:
        G.add_node(event["id"], label=event["name"])

    # 添加边和边的权重
    for activity in data["activities"]:
        G.add_edge(activity["from_event"], activity["to_event"], weight=activity["duration"],
                   label=f"{activity['name']}={activity['duration']}")

    # 绘制AOE网络
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    node_labels = nx.get_node_attributes(G, "label")
    nx.draw(G, pos, with_labels=True, labels=node_labels,
            node_size=1500, node_color="skyblue", font_size=10, arrows=True)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='black')

    plt.title("AOE Network")
    plt.savefig("./out/aoe_network.png")
    plt.show()


if __name__ == "__main__":
    data = json.load(open("aoe_network.json"))
    draw_aoe_network(data)
