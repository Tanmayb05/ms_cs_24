import heapq
import time

# Adjacency list for the Romanian road map
romania_map = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Oradea', 71), ('Arad', 75)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Oradea', 151), ('Arad', 140), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Craiova', 146), ('Pitesti', 97)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

# Heuristic: Straight-line distances to Bucharest (in km)
sld_to_bucharest = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161, 
    'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244, 
    'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193, 
    'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

# Function to estimate SLD using triangle inequality
def estimate_sld_to_goal_city(goal_city, sld_to_bucharest):
    # Check if the goal city exists in the dictionary
    if goal_city not in sld_to_bucharest:
        raise ValueError(f"SLD information for {goal_city} is not available")
    
    sld_goal_city_to_bucharest = sld_to_bucharest[goal_city]  # SLD for the goal city to Bucharest
    
    # Estimating SLD for all other cities to the goal city using triangle inequality
    estimated_sld = {}
    for city, sld_city_to_bucharest in sld_to_bucharest.items():
        if city == goal_city:
            estimated_sld[city] = 0  # SLD from goal city to itself is 0
        else:
            # Use the triangle inequality to estimate the SLD from each city to the goal city
            estimated_sld[city] = sld_city_to_bucharest + sld_goal_city_to_bucharest
    
    return estimated_sld


# Best First Search implementation
def best_first_search(graph, start, goal, heuristic):
    # Priority queue to store (heuristic_value, city, path, total_distance)
    priority_queue = []
    heapq.heappush(priority_queue, (heuristic[start], start, [start], 0))  # (h(n), current city, path, distance traveled)
    
    # Explored set to keep track of visited cities
    explored = set()

    while priority_queue:
        # Pop the city with the smallest heuristic value
        h_value, current_city, path, traveled_distance = heapq.heappop(priority_queue)
        
        # If we reach the goal city, return the path and the total distance
        if current_city == goal:
            return path, traveled_distance
        
        # Mark current city as explored
        explored.add(current_city)

        # Expand neighbors
        for neighbor, distance in graph[current_city]:
            if neighbor not in explored:
                # Add the neighbor to the priority queue with its heuristic and updated path and distance
                new_traveled_distance = traveled_distance + distance
                heapq.heappush(priority_queue, (heuristic[neighbor], neighbor, path + [neighbor], new_traveled_distance))
    
    # Return failure if no path is found
    return [], float('inf')


start_city = 'Timisoara'
goal_city = 'Vaslui'

# Estimate SLDs for all cities to the goal city
if goal_city is not 'Bucharest':
    estimate_sld_to_goal_city_dict = estimate_sld_to_goal_city(goal_city, sld_to_bucharest)
else:
    estimate_sld_to_goal_city_dict = sld_to_bucharest

for city, sld in estimate_sld_to_goal_city_dict.items():
    print(f"Estimated SLD from {city} to {goal_city}: {sld} km")

start_time = time.time()
path, distance = best_first_search(romania_map, start_city, goal_city, estimate_sld_to_goal_city_dict)
end_time = time.time()
total_time = end_time - start_time
print(f"\nPath: {path} \nTotal Distance: {distance} \nTime taken: {total_time:.6f} seconds")

