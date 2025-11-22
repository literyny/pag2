import arcpy
from graph import Graph
from node_edge import Node, Edge

def build_graph(point_lyr, road_lyr, rd_speed, gdb_path, active_map):
    graph = Graph()
    coord_to_id = {}
    vertex_id = 0
    pnts_cls = arcpy.management.CreateFeatureclass(
        gdb_path, point_lyr, "POINT", spatial_reference=2180
    )
    arcpy.management.AddField(pnts_cls, "vertex_id", "LONG")
    i_cursor = arcpy.da.InsertCursor(pnts_cls, ["SHAPE@XY", "vertex_id"])
    with arcpy.da.SearchCursor(road_lyr, ["OBJECTID", "SHAPE@", "KLASA_DROG", "direction"]) as cursor:
        for fid, geom, road_class, direction in cursor:
            start_coord = (round(geom.firstPoint.X, 2), round(geom.firstPoint.Y, 2))
            end_coord = (round(geom.lastPoint.X, 2), round(geom.lastPoint.Y, 2))
            for coord in (start_coord, end_coord):
                if coord not in coord_to_id:
                    n = Node(vertex_id, coord[0], coord[1])
                    graph.add_node(n)
                    i_cursor.insertRow([coord, vertex_id])
                    coord_to_id[coord] = vertex_id
                    vertex_id += 1
            start_node = graph.nodes[coord_to_id[start_coord]]
            end_node = graph.nodes[coord_to_id[end_coord]]
            length = geom.length
            time = (length / rd_speed[road_class]) * 6 / 100
            edge = Edge(fid, start_node, end_node, length, time, direction)
            graph.add_edge(edge)
    del i_cursor
    active_map.addDataFromPath(f"{gdb_path}\\{point_lyr}")
    return graph, point_lyr
