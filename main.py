import arcpy
from graph_builder import build_graph
from forbidden_sequence import ForbiddenSequences
from utils import format_time, get_nearest_vertex_id
from algorithm import Algorithm

gdb_path = arcpy.GetParameterAsText(0)
road_lyr = arcpy.GetParameterAsText(1)
start_pnt = arcpy.GetParameter(2)
end_pnt = arcpy.GetParameter(3)
algorithm_name = arcpy.GetParameterAsText(4)
out_best_path_lyr = arcpy.GetParameter(5)
out_verticles_lyr = arcpy.GetParameter(6)
forbidden_file = arcpy.GetParameterAsText(7)

arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True

active_map = arcpy.mp.ArcGISProject("current").activeMap

rd_speed = {
    "droga dojazdowa": 50,
    "droga główna": 90,
    "droga lokalna": 60,
    "droga wewnętrzna": 30,
    "droga zbiorcza": 70,
    "droga ekspresowa": 120,
    "autostrada": 140,
    "droga główna ruchu przyśpieszonego": 100
}

graph, point_layer_name = build_graph(
    point_lyr="punkty",
    road_lyr=road_lyr,
    rd_speed=rd_speed,
    gdb_path = gdb_path,
    active_map = active_map
)

forbidden = ForbiddenSequences.from_file(forbidden_file, graph)

start_id = get_nearest_vertex_id(start_pnt, point_layer_name)
end_id = get_nearest_vertex_id(end_pnt, point_layer_name)

if start_id is None or end_id is None:
    arcpy.AddMessage("Nie można znaleźć punktu startowego lub końcowego.")
    raise SystemExit

algorithm = Algorithm(graph, forbidden)
if algorithm_name == "Dijkstra":
    result = algorithm.solve_dijkstra(start_id, end_id)

else:
    result = algorithm.solve_a_star(start_id, end_id)

if result is None:
    arcpy.AddMessage("Nie znaleziono żadnej ścieżki.")
    raise SystemExit

time, total_length, vertices, edges, neighbors_checked, visited_cnt = result

edges_expr = f"OBJECTID IN {tuple(edges)}"
verts_expr = f"vertex_id IN {tuple(vertices)}"

arcpy.conversion.ExportFeatures(road_lyr, out_best_path_lyr, edges_expr)
arcpy.conversion.ExportFeatures(point_layer_name, out_verticles_lyr, verts_expr)

arcpy.SetParameterAsText(8, format_time(time))
arcpy.SetParameterAsText(9, f"{total_length/1000:.3f} km")

arcpy.AddMessage(f"""
=== Działanie algorytmu {algorithm_name} ===
Liczba odwiedzonych wierzchołków: {visited_cnt}
Liczba sprawdzonych sąsiadów: {neighbors_checked}
=======================================
""")
