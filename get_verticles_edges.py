import arcpy

def get_verticles_edges(gdb_path, point_lyr, road_lyr, rd_speed, active_map):
    """
    Ekstrahuje listę wierzchołków i listę krawędzi z reprezentacji `graph`.

    Parameters:
        graph: struktura reprezentująca graf – może być słownikiem, listą list, macierzą
               lub inną strukturą zależnie od implementacji.

    Returns:
        tuple:
            (vertices, edges)
            vertices: lista wszystkich wierzchołków w grafie.
            edges: lista krotek (u, v, weight) lub odpowiedniej reprezentacji krawędzi.

    Raises:
        ValueError: jeśli `graph` nie spełnia oczekiwanej struktury lub jest pusta.
    """
    vertex_dict = {} # słownik, gdzie klucz to id wierzchołka, a wartość to współrzędne
    coord_to_id = {} # słownik, gdzie klucz to wspolrzedne, a wartość id wierzchołka
    edge_dict = {} # słownik, gdzie dla id krawędzi jest (id początku, id końca, długość w metrach, czas przejazdu w minutach)
    vertex_id = 0

    pnts_cls = arcpy.management.CreateFeatureclass(gdb_path, point_lyr, "POINT", spatial_reference = 2180)
    arcpy.management.AddField(pnts_cls, "vertex_id", "LONG")
    i_cursor = arcpy.da.InsertCursor(pnts_cls, ['SHAPE@XY', "vertex_id"])

    with arcpy.da.SearchCursor(road_lyr, ['OBJECTID', 'SHAPE@', 'KLASA_DROG']) as cursor:
        for fid, geom, rd_cls in cursor:
            start_coord = (round(geom.firstPoint.X, 2), round(geom.firstPoint.Y, 2))
            end_coord = (round(geom.lastPoint.X, 2), round(geom.lastPoint.Y, 2))

            for coord in [start_coord, end_coord]:
                if coord not in coord_to_id:
                    i_cursor.insertRow([coord, vertex_id])
                    coord_to_id[coord] = vertex_id
                    vertex_dict[vertex_id] = coord
                    vertex_id += 1

            start_id = coord_to_id[start_coord]
            end_id = coord_to_id[end_coord]
            rd_time = (geom.length/rd_speed[rd_cls])*6/100 # czas przejechania drogi w minutach
            edge_dict[fid] = (start_id, end_id, geom.length, rd_time)

        del i_cursor
        active_map.addDataFromPath(f"{gdb_path}\\{point_lyr}")

    return edge_dict, vertex_dict

def read_edge_dict_from_file(file_path):
    edge_dict = {}
    with open(file_path, "r") as file:
        for line in file:
            line_list = line.split(":")
            edge_id = int(line_list[0])
            val = line_list[1].split(",")
            values_tpl = (int(val[0]), int(val[1]), float(val[2]), float(val[3]), val[4].strip())
            edge_dict[edge_id] = values_tpl
    return edge_dict

def prepare_graph(edge_dict):
    graph = {}
    for fid, (u, v, length, time, dirct) in edge_dict.items():
        if dirct == "tam": # jednokierunkowa tam
            graph.setdefault(v, []).append((u, fid))
        elif dirct == "spowrotem": # jednokierunkowa spowrotem
            graph.setdefault(u, []).append((v, fid))
        else: # dwukierunkowa
            graph.setdefault(v, []).append((u, fid))
            graph.setdefault(u, []).append((v, fid))
    return graph