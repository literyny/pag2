from Dijkstra import dijkstra
from get_verticles_edges import get_verticles_edges, read_edge_dict_from_file, prepare_graph
import arcpy
"""
main.py

Punkt wejścia programu. Wykonuje następujące kroki:
1. Wczytuje graf lub dane wejściowe (np. z pliku lub definicji w kodzie).
2. Uruchamia wybrany algorytm grafowy (Dijkstra lub A*).
3. Wyświetla wyniki (ścieżka, koszt, opcjonalnie wizualizacja).

"""
gdb_path = arcpy.GetParameterAsText(0)
point_lyr = arcpy.GetParameterAsText(1)
road_lyr = arcpy.GetParameterAsText(2)
start_id = arcpy.GetParameter(3)
end_id = arcpy.GetParameter(4)
file_path = arcpy.GetParameterAsText(5)

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

for lyr in [point_lyr, road_lyr]:
    arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")


edge_dict = read_edge_dict_from_file(file_path)
graph = prepare_graph(edge_dict)

time, total_length, verticles, edges = dijkstra(start_id, end_id, graph, edge_dict)

if verticles and edges:
    print("Czas [min]: ", round(time, 2), "Długość [km]: ", round(total_length, 2))

    edges_expr = f"OBJECTID IN {tuple(edges)}"
    vrtcls_expr = f"vertex_id IN {tuple(verticles)}"
    
    arcpy.conversion.ExportFeatures(road_lyr, "trasa", edges_expr)
    arcpy.conversion.ExportFeatures(point_lyr, "wierzchołki", vrtcls_expr)
    
    active_map.addDataFromPath(f"{gdb_path}\\trasa")
    active_map.addDataFromPath(f"{gdb_path}\\wierzchołki")
else:
    print("Brak połączenia")