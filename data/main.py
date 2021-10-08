import json
import numpy as np
import time

import os 
print(os.getcwd())
# read data
with open(r"..\data\G.json", encoding = "utf8") as f:
    G = json.load(f)
with open(r"..\data\Dist.json", encoding = "utf8") as f:
    Dist = json.load(f)
with open(r"..\data\Cost.json", encoding = "utf8") as f:
    Cost = json.load(f)
with open(r"..\data\Coord.json", encoding = "utf8") as f:
    Coord = json.load(f)
    
# these functions read the distance and energy of an edge from the data respectively 
def distance_func(u,v):
    return Dist[f"{u},{v}"]
def energy_func(u,v):
    return Cost[f"{u},{v}"]  



"""
TASK 1
"""
from task1 import *

start_time = time.time()
start = "1"
end = "50"
print("Task 1 results:")
dijkstra_shortest_path(G, start, end)
end_time = time.time()
print("Time taken for task 1:", end_time - start_time, "\n")


"""
TASK 2
"""
from task2 import *

start = time.time()
shortest = find_path(G, "1", "50", cost_func=distance_func, energy_func = energy_func, energy_budget = 287932)
end = time.time()
print("Task 2 results:")
print(shortest)
print("Time taken for task 2: ", end - start, "\n")
