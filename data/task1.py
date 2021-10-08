"""
Please ensure that you have import the priority_dictionary.py
"""
from priority_dictionary import *

import os
import json 
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

def dijkstra_task1(graph, start, end=None):
    """Find all shortest paths from start node to a non-specific end, eg: each other node."""
    
    current_total_distances = {}    # dictionary of total distances so far
    candidate_nodes = {}       # dictionary of candidate nodes, where the key is neighbour node, value is current node
    estimated_total_distances = priorityDictionary()     # estimated total distance of so far
    estimated_total_distances[start] = 0        # initialize the distance at start node is 0

    # outer loop
    for current_node in estimated_total_distances:
        current_total_distances[current_node] = estimated_total_distances[current_node]
        if current_node == end:      # if we have reached the end node
            break
            
        neighbours = graph[current_node]
        # inner loop
        # interate through every the current node's every adjacent node
        for neighbour in neighbours:
            # find the updated path_length, which is current total length + distance from current node to its neighbouring node
            path_length = current_total_distances[current_node] + Dist[f"{current_node},{neighbour}"] 
            
            # if the neighbour node has already being visited
            if neighbour in current_total_distances:
                # and the updated path_length is shorter than the previous total distance from start node to neighbour node
                # that means our current route is not the shortest
                if path_length < current_total_distances[neighbour]:
                    # raise rror
                    raise ValueError("Btter path found to an already visited node!")
                    
            # if the neighbour node is not visited 
            # or if the updated path length is shorter than the estimated total distance from start node to neighbour node
            elif neighbour not in estimated_total_distances or path_length < estimated_total_distances[neighbour]:
                # add the neighbour and path_length as key-value pair into the dictionary
                estimated_total_distances[neighbour] = path_length
                # add neighbour and current_node into dictionary
                candidate_nodes[neighbour] = current_node    
                
    return candidate_nodes, estimated_total_distances
    
def dijkstra_shortest_path(graph, start, end):
    """Find a shortest path from start node to the given end node,
    output the list of nodes visited along the shortest path,
    as well as the toal distances and total enegy costs."""
    
    candidate_nodes, estimated_total_distances = dijkstra_task1(graph, start, end)
    shortest_path = []
    while True:
        # append the end node first
        shortest_path.append(end)
        if end == start:
            break
        # retrieve the value in dictionary, which is the end node's adjacent node
        end = candidate_nodes[end]
    # reverse order to get final path
    shortest_path.reverse()
    
    # print out the shortest path
    print("Shortest path:",end = '')
    for i in range(0, len(shortest_path)-1):
        print(shortest_path[i], "->", end = '')
    print(shortest_path[-1], ".") 
    
    # obtain the value in the estimtaed_total_distances dictionary, the end node is the key
    print("Shortest distance:", estimated_total_distances[shortest_path[-1]],".")
    
    # calculate total energy
    total_energy = 0
    for i in range(0, len(shortest_path)-1):
        total_energy += Cost[f"{shortest_path[i]},{shortest_path[i+1]}"] 
    print("Total energy cost:", total_energy, ".")
    # Task 1 does not satisfy the energy constraint



