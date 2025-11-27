import arcpy

def get_path(end_id, prev):
    """
    Rekonstruuje ścieżkę, gdzie:
    prev[node_id] = Edge prowadząca do node_id

    Zwraca:
        total_length : suma długości wszystkich krawędzi
        path_nodes   : lista kolejnych node_id
        path_edges   : lista obiektów Edge w kolejności
    """
    path_nodes = [end_id]
    path_edges = []
    current = end_id

    while current in prev:
        current, edge = prev[current]
        path_edges.append(edge)
        path_nodes.append(current)

    path_nodes.reverse()
    path_edges.reverse()

    total_length = sum(e.length for e in path_edges)

    return total_length, path_nodes, [e.id for e in path_edges]

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

    
def orient_sequence(edge1, edge2):
    """Zwraca listę [first, mid, last], lub None jeśli krawędzie nie są połączone."""
    (u1, v1) = edge1
    (u2, v2) = edge2
    common = {u1, v1} & {u2, v2}
    if not common:
        return None
    mid = common.pop()
    first = u1 if v1 == mid else v1
    last = u2 if v2 == mid else v2
    return [first, mid, last]