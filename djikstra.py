def dijkstra(graph, start):
    # Initialize distances with infinity and set the start node distance to 0
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # Keep track of visited nodes
    visited = []

    while len(visited) < len(graph):
        # Find the unvisited node with the smallest distance
        min_distance = float('infinity')
        current_vertex = None
        for vertex in graph:
            if vertex not in visited and distances[vertex] < min_distance:
                min_distance = distances[vertex]
                current_vertex = vertex

        if current_vertex is None:
            break

        # Visit the node and update the distances of its neighbors
        visited.append(current_vertex)
        for neighbor, weight in graph[current_vertex].items():
            if neighbor not in visited:
                new_distance = distances[current_vertex] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance

    return distances

# Example graph represented as an adjacency list
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Running the inefficient Dijkstra's algorithm
start_node = 'A'
distances = dijkstra(graph, start_node)
print(f"Distances from start node {start_node}: {distances}")

