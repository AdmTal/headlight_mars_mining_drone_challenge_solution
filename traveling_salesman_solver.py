import math

from ortools.constraint_solver import pywrapcp


# Borrowed from
# https://developers.google.com/optimization/routing/tsp

def euclid_distance(x1, y1, x2, y2):
    # Euclidean distance between points.
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return dist


def create_distance_matrix(locations):
    # Create the distance matrix.
    size = len(locations)
    dist_matrix = {}

    for from_node in range(size):
        dist_matrix[from_node] = {}
        for to_node in range(size):
            x1 = locations[from_node][0]
            y1 = locations[from_node][1]
            x2 = locations[to_node][0]
            y2 = locations[to_node][1]
            dist_matrix[from_node][to_node] = euclid_distance(x1, y1, x2, y2)
    return dist_matrix


def create_distance_callback(dist_matrix):
    # Create the distance callback.

    def distance_callback(from_node, to_node):
        return int(dist_matrix[from_node][to_node])

    return distance_callback


def basic_tsp_solution(locations):
    dist_matrix = create_distance_matrix(locations)
    dist_callback = create_distance_callback(dist_matrix)
    tsp_size = len(locations)
    num_routes = 1
    depot = 0

    # Create routing model.
    if tsp_size > 0:
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)
        if not assignment:
            raise Exception('Could not do Traveling Salesman Route')

        route_number = 0
        node = routing.Start(route_number)
        route = []

        while not routing.IsEnd(node):
            route.append(node)
            node = assignment.Value(routing.NextVar(node))
        route.append(0)

    ordered_locations = []
    for index in route:
        ordered_locations.append(locations[index])

    return ordered_locations
