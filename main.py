from Dijkstra import dijkstra
from get_verticles_edges import get_verticles_edges
import arcpy

gdb_path = arcpy.GetParameterAsText(0)
point_lyr = arcpy.GetParameterAsText(1)
road_lyr = arcpy.GetParameterAsText(2)
start_id = arcpy.GetParameter(3)
end_id = arcpy.GetParameter(4)
road_symb = arcpy.GetParameterAsText(5)
vertex_symb = arcpy.GetParameterAsText(6)

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
# print(dijkstra(start_id, end_id, graph, edge_dict))
# print(a_star(start_id, end_id, graph, edge_dict))
active_map.addDataFromPath(f"{gdb_path}\\{point_lyr}")
time, total_length, verticles, edges = dijkstra(start_id, end_id, graph, edge_dict)
if verticles and edges:
    print("Czas [min]: ", round(time, 2), "Długość [km]: ", round(total_length, 2))

    edges_expr = f"OBJECTID IN {tuple(edges)}"
    vrtcls_expr = f"vertex_id IN {tuple(verticles)}"
    
    arcpy.conversion.ExportFeatures(road_lyr, "trasa", edges_expr)
    arcpy.conversion.ExportFeatures(point_lyr, "wierzchołki", vrtcls_expr)
    
    active_map.addDataFromPath(f"{gdb_path}\\trasa")
    active_map.addDataFromPath(f"{gdb_path}\\wierzchołki")
    
    arcpy.management.ApplySymbologyFromLayer("trasa", road_symb)
    arcpy.management.ApplySymbologyFromLayer("wierzchołki", vertex_symb)
else:
    print("Brak połączenia")