from node_edge import Node, Edge

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.adj = {}

    def add_node(self, node: Node):
        self.nodes[node.id] = node
        self.adj.setdefault(node.id, [])

    def add_edge(self, edge: Edge):
        self.edges[edge.id] = edge

        u = edge.start.id
        v = edge.end.id
        dirct = edge.direction

        if dirct == "tam":
            self.adj.setdefault(v, []).append((u, edge))
        elif dirct == "powrot":
            self.adj.setdefault(u, []).append((v, edge))
        else:
            self.adj.setdefault(v, []).append((u, edge))
            self.adj.setdefault(u, []).append((v, edge))

    def neighbors(self, node_id):
        return self.adj.get(node_id, [])

