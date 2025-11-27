from priority_queue import Priority
from utils import get_path

class Algorithm:
    def __init__(self, graph, forbidden_sequences):
        self.graph = graph
        self.forbidden = forbidden_sequences
    
    def solve_dijkstra(self, start_id, end_id):
        pq = Priority(lambda x: x[0]) # kolejka priorytetowa sortuje po czasie
        pq.append((0, start_id))

        visited = set()
        dist = {start_id: 0}
        prev = {}
        neighbors_checked = 0
        
        while len(pq) > 0:
            cost, u = pq.smallest() # bierzemy wierzcholek o najniższym koszcie + koszt

            if u in visited: # usuwamy duplikaty
                continue
            visited.add(u)

            if u == end_id: # jesli znalezlismy cel to koniec
                break

            for v, edge in self.graph.neighbors(u): # analizujemy sąsiadów wierzchołka
                neighbors_checked += 1
                new_cost = cost + edge.time # koszt dojścia do sąsiada

                if self.forbidden.is_blocked(prev, u, v): # jesli zakazane to nie wchodzimy tam
                    continue

                if v not in dist or new_cost < dist[v]:
                    dist[v] = new_cost # koszt dojscia do wierzcholka
                    prev[v] = (u, edge) # poprzednicy i krawedz do nich
                    pq.append((new_cost, v))

        if end_id not in dist: # jesli nie dotarlismy do celu
            return None

        total_len, verts, edges = get_path(end_id, prev) # odtworzenie sciezki

        return dist[end_id], total_len, verts, edges, neighbors_checked, len(visited)

    def heuristic(self, node_id, goal_id):
        n1 = self.graph.nodes[node_id]
        n2 = self.graph.nodes[goal_id]
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        dist = (dx*dx + dy*dy)**0.5
        return (dist / 140) * 6 / 100

    def solve_a_star(self, start_id, end_id):
        pq = Priority(lambda x: x[0])
        pq.append((self.heuristic(start_id, end_id), start_id)) # tu sortowanie po szacowanym czasie
        
        visited = set()
        cost = {start_id: 0}
        prev = {}
        neighbors_checked = 0

        while len(pq) > 0:
            f_u, u = pq.smallest() # bierzemy wierzcholek o najniższym szacowanym koszcie + koszt

            if u in visited:
                continue
            visited.add(u)

            if u == end_id:
                break

            g_u = cost[u]

            for v, edge in self.graph.neighbors(u):
                neighbors_checked += 1
                new_cost = g_u + edge.time

                if self.forbidden.is_blocked(prev, u, v):
                    continue

                if v not in cost or new_cost < cost[v]:
                    cost[v] = new_cost
                    prev[v] = (u, edge)
                    f_cost = new_cost + self.heuristic(v, end_id)
                    pq.append((f_cost, v))

        if end_id not in cost:
            return None

        total_len, verts, edges = get_path(end_id, prev)
        return cost[end_id], total_len, verts, edges, neighbors_checked, len(visited)