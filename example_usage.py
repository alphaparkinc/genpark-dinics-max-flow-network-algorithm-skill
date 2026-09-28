from client import DinicMaxFlow

graph = DinicMaxFlow(4)
graph.add_edge(0, 1, 20)
graph.add_edge(0, 2, 10)
graph.add_edge(1, 2, 5)
graph.add_edge(1, 3, 15)
graph.add_edge(2, 3, 15)

max_f = graph.compute_max_flow(0, 3)
print(f"Max Flow from node 0 to 3: {max_f}")
