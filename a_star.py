import math
from Priority_queue import Priority
from utils import get_path

def heuristic_time(node, goal, vertex_dict):
    x1, y1 = vertex_dict[node]
    x2, y2 = vertex_dict[goal]
    dist = math.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))
    return (dist/140) * 6/100

def a_star(start_id, end_id, graph, edge_dict, heuristic_time=heuristic_time):
    """
        Implementacja algorytmu A* — znajdowanie najkrótszej ścieżki
        od wierzchołka `start` do `goal` w grafie, z wykorzystaniem heurystyki.

        Parameters:
            graph: struktura reprezentująca graf — np. słownik graph[u] = {v: weight_uv, …}.
            start: wierzchołek początkowy.
            goal: wierzchołek docelowy.
            heuristic: funkcja h(u, goal) → estymowany koszt z u do goal (float/int).

        Returns:
            list: ścieżka [start, …, goal] reprezentowana jako lista wierzchołków,
                  jeśli ścieżka istnieje; w przeciwnym razie None lub [].

        Raises:
            ValueError: jeżeli `start` lub `goal` nie znajdują się w grafie.
        """
    pq = Priority(lambda x: x[0])
    pq.append((heuristic_time(start_id, end_id), start_id))

    visited = set()
    cost = {start_id: 0}
    prev = {}
    neighbors_checked = 0
    
    while len(pq) > 0:
        f_u, u = pq.smallest()
        if u in visited:
            continue
        visited.add(u)

        if u == end_id:
            break

        g_u = cost[u]
        
        for v, eid in graph.get(u, []):
            neighbors_checked += 1
            edge_time = edge_dict[eid][3]
            new_cost = g_u + edge_time

            if v not in cost or new_cost < cost[v]:
                cost[v] = new_cost
                prev[v] = (u, eid)
                h_new = heuristic_time(v, end_id)
                f_cost = new_cost + h_new
                pq.append((f_cost, v))

    if end_id not in cost:
        return float('inf'), 0, [], []            
    print("Liczba sprawdzanych sąsiadów: ", neighbors_checked, "\nLiczba różnych przejrzanych wierzchołków: ", len(visited))
    total_length, path_vertices, path_edges = get_path(end_id, prev, edge_dict)
    return cost[end_id], total_length, path_vertices, path_edges