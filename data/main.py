from task3 import *
from task2 import *
from task1 import *
import json
import numpy as np
import time
import os


# read data
with open(r"..\data\G.json", encoding="utf8") as f:
    G = json.load(f)
with open(r"..\data\Dist.json", encoding="utf8") as f:
    Dist = json.load(f)
with open(r"..\data\Cost.json", encoding="utf8") as f:
    Cost = json.load(f)
with open(r"..\data\Coord.json", encoding="utf8") as f:
    Coord = json.load(f)

# these functions read the distance and energy of an edge from the data respectively


def distance_func(u, v):
    return Dist[f"{u},{v}"]


def energy_func(u, v):
    return Cost[f"{u},{v}"]


"""
TASK 1
"""

start = "1"
end = "50"
print("Task 1 results:")
start_time = time.time()
dijkstra_task1(G, start, end)
end_time = time.time()
print("Time taken for task 1:", end_time - start_time, "\n")


"""
TASK 2
"""

start = time.time()
shortest = find_path(G, "1", "50", cost_func=distance_func,
                     energy_func=energy_func, energy_budget=287932)
end = time.time()
print("Task 2 results:")
print("Shortest path: ", "->".join(shortest.nodes))
print("Shortest distance: ", shortest.distance)
print("Total energy cost: ", shortest.energy)
print("Time taken for task 2: ", end - start, "\n")

"""
TASK 3
"""


def heuristic_sl_distance(alpha, node1, node2="50"):
    x_dist = abs(Coord[node1][0])-abs(Coord[node2][0])
    y_dist = abs(Coord[node1][1])-abs(Coord[node2][1])
    dist = math.sqrt(x_dist**2 + y_dist**2)
    return alpha*dist


start = time.time()
shortest = find_path_astar(G, "1", "50", cost_func=distance_func, energy_func=energy_func,
                           heuristic_func=heuristic_sl_distance, alpha=1, energy_budget=287932)
end = time.time()
print("Task 3 results:")
print("Shortest path: ", "->".join(shortest.nodes))
print("Shortest distance: ", shortest.distance)
print("Total energy cost: ", shortest.energy)
print("Time taken for task 2: ", end - start, "\n")
