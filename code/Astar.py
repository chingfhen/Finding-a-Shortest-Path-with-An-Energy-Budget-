from collections import namedtuple
from heapq import heappush, heappop
from inspect import ismethod
from itertools import count

"""
PathInfo 
- final output if path found
- nodes: nodes of the shortest path
- distance: total distance of the path
- energy: total energy of the path
"""
PathInfo = namedtuple("PathInfo", ("nodes", "distance", "energy"))


class DijkstarError(Exception):
    """Base class for Dijkstar errors."""


class NoPathError(DijkstarError):
    """Raised when a path can't be found to a specified node."""


"""
find_path
- finds shortest path from s to d
- wrapper for single_source_shortest_paths
- arguments:
    - graph: an adjacency list
    - cost_func: returns distance from u to v
    - heuristic_func: returns estimated distance from v to d
    - energy_func: returns energy from u to v
    - energy_budget: energy_budget
- Output:
    - PathInfo
"""


def find_path(
    graph, s, d, cost_func, energy_func, heuristic_func=None, energy_budget=287932
):
    if heuristic_func:
        predecessors = astar(
            graph, s, d, cost_func, energy_func, heuristic_func, energy_budget
        )
    else:
        predecessors = single_source_shortest_paths(
            graph, s, d, cost_func, energy_func, heuristic_func, energy_budget
        )

    return extract_shortest_path_from_predecessor_list(predecessors, d)


def find_path_astar(
    graph, s, d, cost_func, energy_func, heuristic_func=None, energy_budget=287932
):

    predecessors = astar(
        graph, s, d, cost_func, energy_func, heuristic_func, energy_budget
    )

    return extract_shortest_path_from_predecessor_list(predecessors, d)


"""
sort_neighbors
- returns list of neighbors sorted based on heuristic value
"""


def sort_neighbors(neighbors, heuristic_func):
    neighbor_dict = {v: heuristic_func(v) for v in neighbors}
    sorted_neighbors = sorted(neighbors, key=neighbor_dict.get)
    return sorted_neighbors


"""
single_source_shortest_paths
- finds shortest path from s to d
- wrapper for single_source_shortest_paths
- arguments:
    - same as find_path
- Output:
    - predecessors: a dictionary of predecessors i.e (predecessor, edge_cost, edge_energy)
"""


def single_source_shortest_paths(
    graph, s, d, cost_func, energy_func, heuristic_func=None, energy_budget=287932
):

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
        visit_queue = [(0, s)]                       # (cost_of_s_to_u, node)
        # visited nodes - guaranteed with the lowest cost_of_s_to_u
        visited = set()

        while visit_queue:

            # gets lowest cost_of_s_to_u
            cost_of_s_to_u, u = heappop(visit_queue)

            if u == d:                               # if u==d, the shortest path is found
                break

            if u in visited:                           # visited nodes are guaranteed to be part of the shortest path
                continue                               # so we don't visit again
            visited.add(u)

            # get the neighbours
            neighbors = graph[u]
            if not neighbors:                                # continue if there are no neighbours
                continue

            # Check each of u's neighboring nodes to see if we can update costs
            for v in neighbors:

                # (visited nodes are guaranteed to have lowest costs already)
                if v in visited:
                    continue

                cost_of_u_to_v = cost_func(u, v)
                cost_of_s_to_u_plus_cost_of_e = cost_of_s_to_u + cost_of_u_to_v

                if heuristic_func:
                    # add "estimated" cost from v to d    ( f = g + h )
                    cost_of_s_to_u_plus_cost_of_e += heuristic_func(v)

                # If there are no existing costs, UPDATE.
                # If the new cost found is lower, UPDATE.
                if v not in costs or cost_of_s_to_u_plus_cost_of_e < costs[v]:
                    # update with lower found cost
                    costs[v] = cost_of_s_to_u_plus_cost_of_e
                    predecessors[v] = (u, cost_of_u_to_v, energy_func(u, v))
                    # push to queue
                    heappush(visit_queue, (cost_of_s_to_u_plus_cost_of_e, v))

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


def astar(graph, s, d, cost_func, energy_func, heuristic_func=None, energy_budget=287932):
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
        # f_scores = {s: heuristic_func(s)}
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
                print('entering loop')
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


"""
extract_shortest_path_from_predecessor_list:
    - arguments:
        - predecessors: information of the shortest path
        - d: destination
    - output:
        - PathInfo: contains shortest path, total distance, total energy
"""


def extract_shortest_path_from_predecessor_list(predecessors, d):

    nodes = [d]    # Nodes on the shortest path from s to d
    costs = []     # costs/distances for shortest path from s to d
    energies = []  # energies for shortest path from s to d
    u, edge_cost, edge_energy = predecessors[d]

    while u is not None:

        nodes.append(u)
        costs.append(edge_cost)
        energies.append(edge_energy)
        u, edge_cost, edge_energy = predecessors[u]

    nodes.reverse()

    return PathInfo(nodes, sum(costs), sum(energies))


"""
extract_energy_from_predecessor_list:
    - arguments:
        - same as extract_shortest_path_from_predecessor_list
    - output:
        - total energy of the shortest path
"""


def extract_energy_from_predecessor_list(predecessors, d):

    energies = []  # energies for shortest path from s to d

    u, _, edge_energy = predecessors[d]

    while u is not None:
        energies.append(edge_energy)
        u, _, edge_energy = predecessors[u]

    return sum(energies)


"""
extract_most_energy_intensive_edge:
    - arguments:
        - same as extract_shortest_path_from_predecessor_list
    - output:
        - most energy intensive edge of the shortest path
"""


def extract_most_energy_intensive_edge(predecessors, d):
    current_most_intensive = (0, 0, 0)
    temp = None
    u, edge_cost, edge_energy = predecessors[d]
    while u is not None:
        if edge_energy > current_most_intensive[2]:
            current_most_intensive = (u, edge_cost, edge_energy)
            key = temp
        temp = u
        u, edge_cost, edge_energy = predecessors[u]
    return f"{current_most_intensive[0]},{key}"
