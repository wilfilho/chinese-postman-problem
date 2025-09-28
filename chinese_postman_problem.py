from collections import defaultdict
import heapq
from functools import lru_cache

graph_edges = [
    ("V1","V2","a1"), ("V2","V3","a2"), ("V3","V4","a3"), ("V4","V5","a4"),
    ("V1","V6","a5"), ("V2","V7","a6"), ("V3","V8","a7"), ("V4","V9","a8"),
    ("V5","V10","a9"), ("V6","V7","a10"), ("V7","V8","a11"), ("V8","V9","a12"),
    ("V9","V10","a13"), ("V6","V15","a14"), ("V7","V11","a15"), ("V11","V12","a16"),
    ("V10","V12","a17"), ("V11","V13","a18"), ("V13","V14","a19"), ("V12","V14","a20"),
    ("V15","V16","a21"), ("V13","V16","a22"), ("V16","V17","a23"), ("V17","V18","a24"),
    ("V18","V19","a25"), ("V14","V19","a26"), ("V15","V24","a27"), ("V16","V20","a28"),
    ("V20","V21","a29"), ("V21","V22","a30"), ("V19","V22","a31"), ("V20","V23","a32"),
    ("V21","V23","a33"), ("V23","V25","a34"), ("V24","V25","a35"),
]

def build_adjacency_list(edges_list):
    """
    Builds adjacency list from edges.
    
    Args:
        edges_list: List of tuples (source, target, label)
    
    Returns:
        defaultdict: Adjacency list where each vertex maps to list of neighbors
    """
    adjacency_list = defaultdict(list)
    for source_vertex, target_vertex, edge_label in edges_list:
        adjacency_list[source_vertex].append((target_vertex, 1, edge_label))
        adjacency_list[target_vertex].append((source_vertex, 1, edge_label))
    return adjacency_list

def dijkstra(adjacency_list, source_vertex):
    """
    Calculates shortest distances from a source vertex to all others.
    
    Args:
        adjacency_list: Graph adjacency list
        source_vertex: Source vertex
    
    Returns:
        tuple: (distances, predecessors)
    """
    distances = {vertex: float("inf") for vertex in adjacency_list}
    predecessors = {vertex: None for vertex in adjacency_list}
    distances[source_vertex] = 0
    
    priority_queue = [(0, source_vertex)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance != distances[current_vertex]:
            continue
            
        for neighbor_vertex, edge_weight, _ in adjacency_list[current_vertex]:
            new_distance = current_distance + edge_weight
            if new_distance < distances[neighbor_vertex]:
                distances[neighbor_vertex] = new_distance
                predecessors[neighbor_vertex] = current_vertex
                heapq.heappush(priority_queue, (new_distance, neighbor_vertex))
    
    return distances, predecessors

def reconstruct_shortest_path(predecessors, start_vertex, end_vertex):
    """
    Reconstructs the shortest path between two vertices.
    
    Args:
        predecessors: Dijkstra predecessors dictionary
        start_vertex: Starting vertex
        end_vertex: Ending vertex
    
    Returns:
        list: Path from start to end
    """
    path = []
    current_vertex = end_vertex
    
    while current_vertex is not None:
        path.append(current_vertex)
        if current_vertex == start_vertex:
            break
        current_vertex = predecessors[current_vertex]
    
    return list(reversed(path))

def hierholzer(adjacency_list, starting_vertex):
    """
    Finds Eulerian circuit using Hierholzer's algorithm.
    
    Args:
        adjacency_list: Graph adjacency list (must be Eulerian)
        starting_vertex: Starting vertex of the circuit
    
    Returns:
        list: Eulerian circuit
    """
    vertex_stack = [starting_vertex]
    eulerian_circuit = []
    used_edges = set()
    
    next_edge_index = {vertex: 0 for vertex in adjacency_list}
    
    while vertex_stack:
        current_vertex = vertex_stack[-1]
        
        while (next_edge_index[current_vertex] < len(adjacency_list[current_vertex]) and 
               (current_vertex, 
                adjacency_list[current_vertex][next_edge_index[current_vertex]][0], 
                adjacency_list[current_vertex][next_edge_index[current_vertex]][2]) in used_edges):
            next_edge_index[current_vertex] += 1
        
        if next_edge_index[current_vertex] == len(adjacency_list[current_vertex]):
            eulerian_circuit.append(current_vertex)
            vertex_stack.pop()
        else:
            neighbor_vertex, _, edge_label = adjacency_list[current_vertex][next_edge_index[current_vertex]]
            
            if (current_vertex, neighbor_vertex, edge_label) in used_edges:
                next_edge_index[current_vertex] += 1
                continue
            
            used_edges.add((current_vertex, neighbor_vertex, edge_label))
            used_edges.add((neighbor_vertex, current_vertex, edge_label))
            vertex_stack.append(neighbor_vertex)
    
    return eulerian_circuit[::-1]

def chinese_postman_problem(edges_list, starting_vertex="V1"):
    """
    Solves the Chinese Postman Problem.
    
    Args:
        edges_list: List of graph edges
        starting_vertex: Starting vertex of the tour
    
    Returns:
        dict: Result containing total cost and tour
    """
    adjacency_list = build_adjacency_list(edges_list)
    
    vertex_degrees = {vertex: len(adjacency_list[vertex]) for vertex in adjacency_list}
    odd_degree_vertices = [vertex for vertex in adjacency_list if vertex_degrees[vertex] % 2 == 1]

    if not odd_degree_vertices:
        eulerian_tour = hierholzer(build_adjacency_list(edges_list), starting_vertex)
        return {
            "total_cost": len(edges_list),
            "tour": eulerian_tour
        }

    all_shortest_paths_data = {}
    for odd_vertex in odd_degree_vertices:
        distances, predecessors = dijkstra(adjacency_list, odd_vertex)
        all_shortest_paths_data[odd_vertex] = (distances, predecessors)

    num_odd_vertices = len(odd_degree_vertices)
    
    odd_distances_matrix = [[0] * num_odd_vertices for _ in range(num_odd_vertices)]
    odd_paths_matrix = [[None] * num_odd_vertices for _ in range(num_odd_vertices)]
    
    for i, source_odd_vertex in enumerate(odd_degree_vertices):
        for j, target_odd_vertex in enumerate(odd_degree_vertices):
            if i == j:
                continue
            odd_distances_matrix[i][j] = all_shortest_paths_data[source_odd_vertex][0][target_odd_vertex]
            odd_paths_matrix[i][j] = reconstruct_shortest_path(
                all_shortest_paths_data[source_odd_vertex][1], 
                source_odd_vertex, 
                target_odd_vertex
            )

    @lru_cache(None)
    def find_minimum_matching(available_vertices_bitmask):
        """
        Finds minimum cost matching using DP with bitmask.
        
        Args:
            available_vertices_bitmask: Bitmask representing available vertices
        
        Returns:
            tuple: (minimum_cost, list_of_pairs)
        """
        if available_vertices_bitmask == 0:
            return (0, [])
        
        first_available_index = (available_vertices_bitmask & -available_vertices_bitmask).bit_length() - 1
        best_cost = float("inf")
        best_pairing = []
        
        remaining_mask = available_vertices_bitmask & ~(1 << first_available_index)
        
        for second_vertex_index in range(first_available_index + 1, num_odd_vertices):
            if remaining_mask & (1 << second_vertex_index):
                new_available_mask = remaining_mask & ~(1 << second_vertex_index)
                
                subproblem_cost, subproblem_pairs = find_minimum_matching(new_available_mask)
                
                pair_cost = odd_distances_matrix[first_available_index][second_vertex_index]
                candidate_solution = (
                    subproblem_cost + pair_cost, 
                    subproblem_pairs + [(first_available_index, second_vertex_index)]
                )
                

                if candidate_solution[0] < best_cost:
                    best_cost = candidate_solution[0]
                    best_pairing = candidate_solution[1]
        
        return (best_cost, best_pairing)
    full_vertices_bitmask = (1 << num_odd_vertices) - 1
    matching_cost, matching_pairs = find_minimum_matching(full_vertices_bitmask)

    multigraph_adjacency = build_adjacency_list(edges_list)
    duplicate_edge_counter = 100
    
    def add_path_to_multigraph(vertex_path):
        nonlocal duplicate_edge_counter
        for current_vertex, next_vertex in zip(vertex_path, vertex_path[1:]):
            duplicate_label = f"dup{duplicate_edge_counter}"
            multigraph_adjacency[current_vertex].append((next_vertex, 1, duplicate_label))
            multigraph_adjacency[next_vertex].append((current_vertex, 1, duplicate_label))
            duplicate_edge_counter += 1

    for (first_index, second_index) in matching_pairs:
        path_between_paired_vertices = odd_paths_matrix[first_index][second_index]
        add_path_to_multigraph(path_between_paired_vertices)

    final_eulerian_tour = hierholzer(multigraph_adjacency, starting_vertex)
    total_tour_cost = len(edges_list) + matching_cost
    
    return {
        "total_cost": total_tour_cost,
        "odd_vertices": odd_degree_vertices,
        "paired": [(odd_degree_vertices[i], odd_degree_vertices[j]) for i, j in matching_pairs],
        "tour": final_eulerian_tour
    }

if __name__ == "__main__":
    solution_result = chinese_postman_problem(graph_edges, starting_vertex="V1")
    
    print(f"Total cost: {solution_result['total_cost']}")
    print(f"Tour: {solution_result['tour']}")
