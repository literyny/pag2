from Priority_queue import Priority
from utils import get_path

def dijkstra(start_id, end_id, graph, edge_dict):
    """
       Implementacja algorytmu Dijkstry — znajdowanie najkrótszych ścieżek
       od źródła `start` do wszystkich innych wierzchołków w grafie.

       Parameters:
           graph: struktura reprezentująca graf — najczęściej słownik,
                  gdzie graph[u] = {v: weight_uv, …} reprezentuje krawędzie u→v z wagą weight_uv.
           start: wierzchołek początkowy (klucz występujący w graph).

       Returns:
           tuple:
               (distances, previous)
               distances: dict {v: cost} — koszt najtańszej ścieżki ze `start` do v.
               previous: dict {v: u} — poprzednik v w najkrótszej ścieżce ze `start`.

       Raises:
           ValueError: jeżeli `start` nie znajduje się w grafie.
       """
    pq = Priority(lambda x: x[0]) # dodajemy do kolejki kolejnych sąsiadów, jeśli ścieżka się poprawi
    pq.append((0, start_id)) # dodajemy pierwszy wierzchołek (czas, id)
    
    visited = set()
    dist = {start_id: 0} # czas najkrótszej ścieżki od start_id do aktualnego
    prev = {} # poprzednicy do odtworzenia
    neighbors_checked = 0 # do sprawdzania jak szybko działa

    while len(pq) > 0: # dopóki kolejka nie jest pusta
        cost, u = pq.smallest() # ściągamy minimum z kolejki
        if u in visited:
            continue
        visited.add(u)

        if u == end_id:
            break

        for v, eid in graph.get(u, []): # v to sąsiad, eid to krawędź prowadząca do sąsiada
            neighbors_checked += 1
            edge_time = edge_dict[eid][3]
            new_cost = cost + edge_time

            if v not in dist or new_cost < dist[v]: # jeśli nie mamy długości trasy do wierzchołka, albo znaleźliśmy krótszą trasę
                dist[v] = new_cost # dodajemy najkrótszą ścieżkę od start_id do wierzchołka
                prev[v] = (u, eid) # dla wierzchołka trzymamy jego poprzednika i krawędź, która do niego prowadzi
                pq.append((new_cost, v)) # to może lepiej update'ować zamiast dodawać? Jak złożoność?

    if end_id not in dist:
        return float('inf'), 0, [], []            

    # odtwarzanie ścieżki
    total_length, path_vertices, path_edges = get_path(end_id, prev, edge_dict)
    print("Liczba sprawdzanych sąsiadów: ", neighbors_checked, "\nLiczba różnych przejrzanych wierzchołków: ", len(visited))
    return dist[end_id], total_length, path_vertices, path_edges