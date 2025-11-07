import arcpy

def get_path(end_id, prev, edge_dict):
    """
    Odtwarza ścieżkę od wierzchołka `start` do wierzchołka `goal`
    korzystając z mapowania `came_from`, jakie powstało w trakcie algorytmu przeszukiwania.

    Parameters:
        came_from: dict zawierający dla każdego wierzchołka v klucz „poprzednik” w ścieżce
                   (came_from[v] = u ⇒ ścierzka prowadzi przez u do v).
        start: wierzchołek początkowy.
        goal: wierzchołek docelowy.

    Returns:
        list: lista wierzchołków od `start` do `goal` włącznie,
              jeżeli istnieje ścieżka. Jeśli nie istnieje, może zwrócić pustą listę lub None.

    Raises:
        KeyError: jeśli `goal` nie występuje w `came_from` i nie jest równo startowi.
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
    """Zwraca vertex_id najbliższego punktu w warstwie."""
    temp_fc = arcpy.management.CopyFeatures(
        input_point,
        arcpy.CreateScratchName("tmp_point", data_type="FeatureClass", workspace=arcpy.env.scratchGDB)
    )
    arcpy.analysis.Near(temp_fc, target_layer)
    with arcpy.da.SearchCursor(temp_fc, ["NEAR_FID"]) as c:
        near_fid = next(c)[0]
    where = f"OBJECTID = {near_fid}"
    with arcpy.da.SearchCursor(target_layer, ["vertex_id"], where_clause=where) as c:
        vertex_id = next(c)[0]
    arcpy.management.Delete(temp_fc)
    return vertex_id