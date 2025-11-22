class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x = x
        self.y = y

class Edge:
    def __init__(self, edge_id, start, end, length, time, direction):
        self.id = edge_id
        self.start = start
        self.end = end
        self.length = length
        self.time = time
        self.direction = direction
