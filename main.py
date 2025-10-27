from Dijkstra import dijkstra
import a_star
from get_verticles_edges import get_verticles_edges
from a_star import a_star, heuristic_time

gdb_path = "C:\\pag\\MyProject\\MyProject.gdb"
point_lyr = "punkty"
road_lyr = "drogi"
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
           "droga główna ruchu przyspieszonego": 100}

for lyr in [point_lyr, road_lyr]:
    arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")

graph, edge_dict, vertex_dict = get_verticles_edges(gdb_path, point_lyr, road_lyr, rd_speed)

print(dijkstra(1, 155, graph, edge_dict))
print(a_star(1, 155, graph, edge_dict))

time, total_length, verticles, edges = dijkstra(105, 21, graph, edge_dict)
if verticles and edges:
    print("Czas [min]: ", round(time, 2), "Długość [km]: ", round(total_length, 2))

    edges_expr = f"OBJECTID IN {tuple(edges)}"
    vrtcls_expr = f"vertex_id IN {tuple(verticles)}"

    arcpy.conversion.ExportFeatures(f"{gdb_path}\\{road_lyr}", "trasa", edges_expr)
    arcpy.conversion.ExportFeatures(f"{gdb_path}\\{point_lyr}", "wierzchołki", vrtcls_expr)

    arcpy.management.ApplySymbologyFromLayer("trasa", "C:\\pag\\MyProject\\trasa.lyrx")
    arcpy.management.ApplySymbologyFromLayer("wierzchołki", "C:\\pag\\MyProject\\wierzchołki.lyrx")
else:
    print("Brak połączenia")