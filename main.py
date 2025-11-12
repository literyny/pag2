from Dijkstra import dijkstra
from a_star import a_star, heuristic_time
from get_verticles_edges import get_verticles_edges, prepare_graph
from utils import get_nearest_vertex_id, format_time
import arcpy

gdb_path = arcpy.GetParameterAsText(0)
road_lyr = arcpy.GetParameterAsText(1)
start_pnt = arcpy.GetParameter(2)
end_pnt = arcpy.GetParameter(3)
algorithm = arcpy.GetParameterAsText(4)
out_best_path_lyr = arcpy.GetParameter(5)
out_verticles_lyr = arcpy.GetParameter(6)

arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

active_map = arcpy.mp.ArcGISProject("current").activeMap

rd_speed = {"droga dojazdowa": 50,
           "droga główna": 90,
           "droga lokalna": 60,
           "droga wewnętrzna": 30,
           "droga zbiorcza": 70,
           "droga ekspresowa": 120,
           "autostrada": 140,
           "droga główna ruchu przyśpieszonego": 100}

new_verticles_lyr = "punkty"

edge_dict, vertex_dict = get_verticles_edges(gdb_path, new_verticles_lyr, road_lyr, rd_speed, active_map)
graph = prepare_graph(edge_dict)

start_id = get_nearest_vertex_id(start_pnt, new_verticles_lyr)
end_id = get_nearest_vertex_id(end_pnt, new_verticles_lyr)

if start_id and end_id:
    if algorithm == "A*":
        time, total_length, verticles, edges, neighbors_checked, visited_cnt = a_star(
            start_id=start_id,
            end_id=end_id,
            graph=graph,
            edge_dict=edge_dict,
            vertex_dict=vertex_dict,
            heuristic_time=heuristic_time
        )
    elif algorithm == "Dijkstra":
        time, total_length, verticles, edges, neighbors_checked, visited_cnt = dijkstra(
            start_id=start_id,
            end_id=end_id,
            graph=graph,
            edge_dict=edge_dict
        )
    if time and total_length and verticles and edges:
        edges_expr = f"OBJECTID IN {tuple(edges)}"
        vrtcls_expr = f"vertex_id IN {tuple(verticles)}"
        
        arcpy.conversion.ExportFeatures(road_lyr, out_best_path_lyr, edges_expr)
        arcpy.conversion.ExportFeatures(new_verticles_lyr, out_verticles_lyr, vrtcls_expr)
        arcpy.SetParameterAsText(7, format_time(time))
        arcpy.SetParameterAsText(8, f"{total_length/1000:.3f} km")

        arcpy.AddMessage(f"""
=== DZIAŁANIE ALGORYTMU ===
Liczba sprawdzanych sąsiadów: {neighbors_checked}
Liczba różnych przejrzanych wierzchołków: {visited_cnt}
=============================
""")
        