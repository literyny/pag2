from Dijkstra import dijkstra
from a_star import a_star, heuristic_time
from get_verticles_edges import get_verticles_edges, read_edge_dict_from_file, prepare_graph
from utils import get_nearest_vertex_id
import arcpy

gdb_path = arcpy.GetParameterAsText(0)
point_lyr = arcpy.GetParameterAsText(1)
road_lyr = arcpy.GetParameterAsText(2)
start_pnt = arcpy.GetParameter(3)
end_pnt = arcpy.GetParameter(4)

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

edge_dict, vertex_dict = get_verticles_edges(gdb_path, point_lyr, road_lyr, rd_speed, active_map)
graph = prepare_graph(edge_dict)

start_id = get_nearest_vertex_id(start_pnt, point_lyr)
end_id = get_nearest_vertex_id(end_pnt, point_lyr)

time, total_length, verticles, edges = a_star(
    start_id=start_id,
    end_id=end_id,
    graph=graph,
    edge_dict=edge_dict,
    vertex_dict=vertex_dict,
    heuristic_time=heuristic_time
)

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