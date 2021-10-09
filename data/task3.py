# %%
import math
import time
import json

# use util functions from task 2
from task2 import *
from heapq import heappush


def find_path_astar(
    graph, s, d, cost_func, energy_func, heuristic_func, energy_budget=287932
):

    predecessors = astar(
        graph, s, d, cost_func, energy_func, heuristic_func, energy_budget
    )

    return extract_shortest_path_from_predecessor_list(predecessors, d)


def astar(graph, s, d, cost_func, energy_func, heuristic_func, energy_budget=287932):
    # optional - allows the algorithm to rerun multiple times
    graph = graph.copy()

    while True:
        """
        following block of code:
            - finds the shortest path 
            - shortest path information is found in predecessors
        """
        costs = {
            s: 0}                               # Current known costs of paths from s to all nodes
        # (predecessor, edge_cost, edge_energy)
        predecessors = {s: (None, None, None)}

        # (f_score of u, cost_of_s_to_u, node)
        visit_queue = [(heuristic_func(s), 0, s)]

        # visited nodes - guaranteed with the lowest cost_of_s_to_u
        visited = set()

        while visit_queue:

            # gets lowest cost_of_s_to_u
            _, cost_of_s_to_u, u = heappop(visit_queue)

            if u == d:
                # if u==d, the shortest path is found
                break

            if u in visited:                           # visited nodes are guaranteed to be part of the shortest path
                continue                               # so we don't visit again
            visited.add(u)

            # get the neighbours
            neighbors = graph[u]
            if not neighbors:                                # continue if there are no neighbours
                continue

            # sort neighbours based on heuristic
            neighbors = sort_neighbors(neighbors, heuristic_func)

            # Check each of u's neighboring nodes to see if we can update costs
            for v in neighbors:

                # (visited nodes are guaranteed to have lowest costs already)
                if v in visited:
                    continue

                cost_of_u_to_v = cost_func(u, v)
                cost_of_s_to_u_plus_cost_of_e = cost_of_s_to_u + cost_of_u_to_v

                # add "estimated" cost from v to d    ( f = g + h )

                f_score = cost_of_s_to_u_plus_cost_of_e + heuristic_func(v)

                # If there are no existing costs, UPDATE.
                # If the new cost found is lower, UPDATE.
                if v not in costs or cost_of_s_to_u_plus_cost_of_e < costs[v]:
                    # update with lower found cost
                    costs[v] = cost_of_s_to_u_plus_cost_of_e
                    predecessors[v] = (u, cost_of_u_to_v, energy_func(u, v))
                    # push to queue

                    heappush(
                        visit_queue, (f_score, cost_of_s_to_u_plus_cost_of_e, v))

        """
        following block of code:
            - checks if shortest path found exceed the budget
            - if so, remove the most energy intensive edge of the shortest path from the Graph
            - restart 
        """
        if energy_budget:
            if extract_energy_from_predecessor_list(predecessors, d) > energy_budget:
                most_energy_intensive_edge = extract_most_energy_intensive_edge(
                    predecessors, d)
                a, b = most_energy_intensive_edge.split(",")
                graph[a].remove(b)
            else:
                break                    # break if budget requirement is met
        else:
            break                        # break if there is no budget requirement

    if d is not None and d not in costs:
        raise NoPathError("Could not find a path from {0} to {1}".format(s, d))

    return predecessors


def sort_neighbors(neighbors, heuristic_func):
    neighbor_dict = {v: heuristic_func(v) for v in neighbors}
    sorted_neighbors = sorted(neighbors, key=neighbor_dict.get)
    return sorted_neighbors


with open(r"../data/G.json", encoding="utf8") as f:
    G = json.load(f)
with open(r"../data/Dist.json", encoding="utf8") as f:
    Dist = json.load(f)
with open(r"../data/Cost.json", encoding="utf8") as f:
    Cost = json.load(f)
with open(r"../data/Coord.json", encoding="utf8") as f:
    Coord = json.load(f)


def distance_func(u, v):
    return Dist[f"{u},{v}"]


def energy_func(u, v):
    return Cost[f"{u},{v}"]


def heuristic_sl_distance(node1, node2="50", alpha=1):
    x_dist = abs(Coord[node1][0])-abs(Coord[node2][0])
    y_dist = abs(Coord[node1][1])-abs(Coord[node2][1])
    dist = math.sqrt(x_dist**2 + y_dist**2)
    return alpha * dist


# %%
# A* single run
start = time.time()
shortest = find_path_astar(G, "1", "50", cost_func=distance_func, energy_func=energy_func,
                           heuristic_func=heuristic_sl_distance, energy_budget=287932)
end = time.time()
print(shortest)
print(end-start)

# %%
# average time for 100 runs heuristic A*
times = []
for i in range(100):
    start = time.time()
    shortest = find_path_astar(G, "1", "50", cost_func=distance_func, energy_func=energy_func,
                               heuristic_func=heuristic_sl_distance, energy_budget=287932)
    end = time.time()
    times.append(end-start)

avg_time = sum(times)/len(times)
print(avg_time)

# %%
