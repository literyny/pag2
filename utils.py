def get_path(end_id, prev, edge_dict):
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