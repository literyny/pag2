import arcpy

def get_path(end_id, prev, edge_dict):
    """
    Rekonstruuje najkrótszą ścieżkę od startu do end_id na podstawie słownika prev.

    Args:
        end_id (int): identyfikator węzła końcowego.
        prev (dict): mapa poprzedników {node: (prev_node, edge_id)}.
        edge_dict (dict): mapa krawędzi {edge_id: (u, v, length, time, direction)}

    Returns:
        total_length (float): długość trasy w metrach
        path_vertices (list): lista id wierzchołków na ścieżce
        path_edges (list): lista id krawędzi na ścieżce
    """
    path_vertices = [end_id]
    path_edges = []
    u = end_id
    while u in prev:
        u, eid = prev[u]
        path_vertices.append(u)
        path_edges.append(eid)

    path_vertices.reverse()
    path_edges.reverse()

    total_length = sum(edge_dict[eid][2] for eid in path_edges)
    
    return total_length, path_vertices, path_edges


def get_nearest_vertex_id(input_point, target_layer):
    """
    Znajduje wartość atrybutu vertex_id najbliższego wierzchołka 
    na warstwie target_layer względem podanego punktu (input_point). 
    Punkt musi leżeć w promieniu 1 km od najbliższego punktu na warstwie

    Args:
        input_point (PointGeometry): punkt wejściowy
        target_layer (str): nazwa lub ścieżka do warstwy wierzchołków

    Returns:
        int: vertex_id najbliższego wierzchołka
    """
    arcpy.analysis.Near(input_point, target_layer, "1000 METERS")
    with arcpy.da.SearchCursor(input_point, ["NEAR_FID"]) as cursor:
        near_fid = next(cursor)[0]
    if near_fid !=-1:
        where = f"OBJECTID = {near_fid}"
        with arcpy.da.SearchCursor(target_layer, ["vertex_id"], where_clause=where) as cursor:
            vertex_id = next(cursor)[0]
        return vertex_id
    else:
        return None
    
def format_time(minutes):
    """Zwraca czas w formacie H M S na podstawie liczby minut."""
    total_seconds = int(minutes * 60)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours} h")
    if minutes > 0 or hours > 0:
        parts.append(f"{minutes} min")
    parts.append(f"{seconds} s")

    return " ".join(parts)

def is_forbidden(prev, u, v, forbidden_sequences):
    """
    prev – słownik poprzedników: child -> (parent, edge)
    u – aktualny węzeł
    v – proponowany następny węzeł
    forbidden_sequences – lista sekwencji zakazanych (listy int)
    """

    for seq in forbidden_sequences:
        k = len(seq)

        # Ostatni element w sekwencji musi się zgadzać
        if seq[-1] != v:
            continue

        # Odtwarzamy końcówkę ścieżki o długości k
        suffix = get_suffix(prev, u, k - 1) + [v]

        # Jeśli końcówka ścieżki równa zakazowi blokujemy
        if suffix == seq:
            return True

    return False

def get_suffix(prev, last_node, length):
    seq = [last_node]
    curr = last_node

    for _ in range(length - 1):
        if curr not in prev:
            break
        curr, _ = prev[curr]
        seq.append(curr)

    return seq[::-1]


def read_forbidden(file, edge_dict):
    """Funkcja czyta id odcinków z pliku i tworzy sekwencje zakazanych wierzchołków."""
    all_sequences = []

    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            vertexes = []
            prev_edge = None
            oriented = False # czy ustaliliśmy już orientację sekwencji - tzn czy przeszlismy 2 pierwsze iteracje
            skip_line = False # jesli dane będą nie poprawne to będziemy pomijać linię

            for el in line.split():
                edge = edge_dict[int(el)]
                if edge is None:
                    skip_line = True
                    break

                u, v = edge[:2]
                

                if prev_edge is None: # pierwsza iteracja
                    prev_edge = (u, v)
                    continue

                if not oriented: # druga iteracja
                    pu, pv = prev_edge

                    common = {pu, pv} & {u, v} # powtarzający się wierzchołek w dwóch krawędziach
                    if not common:
                        skip_line = True
                        break

                    mid = common.pop()
                    first = pu if pv == mid else pv # niepowtarzający się wierzchołek poprzednika jest pierwszym wierzchołkiem sekwencji
                    last = u if v == mid else v # niepowtarzający się wierzchołek aktualnego jest ostatnim wierzchołkiem sekwencji

                    vertexes = [first, mid, last]
                    oriented = True

                else: # pozostałe iteracje
                    seq_last = vertexes[-1]

                    if u == seq_last:
                        new_vertex = v
                    elif v == seq_last:
                        new_vertex = u
                    else:
                        skip_line = True
                        break

                    vertexes.append(new_vertex)

                prev_edge = (u, v)

            if not skip_line and vertexes:
                all_sequences.append(vertexes)

    return all_sequences