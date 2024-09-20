import heapq
import time
import tracemalloc
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# plot graph coordinates
# https://gist.github.com/parthi2929/27168746d6bfe10a350227c277b2a9c8#file-romania_helper_ipython-py

class RomaniaMap:
    def __init__(self):
        self.map = {
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

        self.sld_to_bucharest = {
            'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161,
            'Fagaras': 176, 'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244,
            'Mehadia': 241, 'Neamt': 234, 'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193,
            'Sibiu': 253, 'Timisoara': 329, 'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
        }

        # Romania's cities and their positions
        self.romania_location_map = {
            'A' : {'pos': (21.31227,46.18656), 'connections': ['S','T','Z'] },
            'S' : {'pos': (24.12558,45.79833), 'connections': ['F','RV','O'] },
            'Z' : {'pos': (21.51742,46.62251), 'connections': ['O'] },
            'T' : {'pos': (21.20868,45.74887), 'connections': ['L'] },
            'O' : {'pos': (21.91894,47.04650), 'connections': [] },
            'F' : {'pos': (24.97310,45.84164), 'connections': ['B'] },
            'L' : {'pos': (21.90346,45.69099), 'connections': ['M'] },
            'RV' : {'pos': (24.36932,45.09968), 'connections': ['C','P'] },
            'M' : {'pos': (22.36452,44.90411), 'connections': ['D'] },
            'D' : {'pos': (22.65973,44.63692), 'connections': ['C'] },
            'C' : {'pos': (23.79488,44.33018), 'connections': [] },
            'P' : {'pos': (24.86918,44.85648), 'connections': ['B','C'] },
            'B' : {'pos': (26.10254,44.42677), 'connections': ['G','U'] },
            'G' : {'pos': (25.96993,43.90371), 'connections': [] },
            'U' : {'pos': (26.64112,44.71653), 'connections': ['H','V'] },
            'V' : {'pos': (27.72765,46.64069), 'connections': ['I'] },
            'I' : {'pos': (27.60144,47.15845), 'connections': ['N'] },
            'N' : {'pos': (26.38188,46.97587), 'connections': [] },
            'H' : {'pos': (27.94566,44.68935), 'connections': ['E'] },
            'E' : {'pos': (28.65273,44.04911), 'connections': [] }
        }

    # Calculate distances between two cities
    @staticmethod
    def calculate_distance(pos1, pos2):
        return round(geodesic((pos1[1], pos1[0]), (pos2[1], pos2[0])).kilometers, 2)

    # Create the graph and add distances as edge labels
    def load_map_graph_with_distances(self, map_dict):
        G = nx.Graph()
        for city, data in map_dict.items():
            G.add_node(city, pos=data['pos'])
            for neighbor in data['connections']:
                distance = self.calculate_distance(map_dict[city]['pos'], map_dict[neighbor]['pos'])
                G.add_edge(city, neighbor, weight=distance)
        return G

    # Function to plot the graph with highlighted path and distances
    @staticmethod
    def plot_graph_with_path_and_distances(G, path=None):
        pos = nx.get_node_attributes(G, 'pos')  # Extract positions
        plt.figure(figsize=(12, 10))

        # Draw the entire graph
        nx.draw(G, pos, node_color='skyblue', with_labels=True, node_size=500, font_size=10, font_weight='bold', font_color='black')
        nx.draw_networkx_edges(G, pos, edge_color='gray')

        # Draw edge labels (distances)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size = 8, font_color='green', verticalalignment='bottom')

        # Highlight the path if provided
        if path:
            # Highlight the nodes in the path
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', node_size=500)

            # Highlight the edges in the path
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

        plt.title('Romania Map with Highlighted Path and Distances')
        plt.show()


    def estimate_sld_to_goal_city(self, goal_city):
        if goal_city not in self.sld_to_bucharest:
            raise ValueError(f"SLD information for {goal_city} is not available")

        sld_goal_city_to_bucharest = self.sld_to_bucharest[goal_city]
        estimated_sld = {city: (self.sld_to_bucharest[city] + sld_goal_city_to_bucharest
                                if city != goal_city else 0)
                          for city in self.sld_to_bucharest}
        return estimated_sld

    @staticmethod
    def depth_first_search(graph, start, goal):
        stack = [(start, [start])]
        visited = set()

        while stack:
            current_city, path = stack.pop()
            if current_city not in visited:
                visited.add(current_city)
                if current_city == goal:
                    return path
                for neighbor, _ in graph[current_city]:
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))

        return None

    @staticmethod
    def calculate_total_distance(path, graph):
        total_distance = 0
        for i in range(len(path) - 1):
            city, next_city = path[i], path[i + 1]
            for neighbor, distance in graph[city]:
                if neighbor == next_city:
                    total_distance += distance
                    break
            else:
                raise ValueError(f"No direct route from {city} to {next_city}")
        return total_distance

    @staticmethod
    def best_first_search(graph, start, goal, heuristic):
        priority_queue = []
        heapq.heappush(priority_queue, (heuristic[start], start, [start], 0))
        explored = set()

        while priority_queue:
            h_value, current_city, path, traveled_distance = heapq.heappop(priority_queue)

            if current_city == goal:
                return path, traveled_distance

            explored.add(current_city)

            for neighbor, distance in graph[current_city]:
                if neighbor not in explored:
                    new_traveled_distance = traveled_distance + distance
                    heapq.heappush(priority_queue, (heuristic[neighbor], neighbor, path + [neighbor], new_traveled_distance))

        return [], float('inf')

    def run_searches(self, start_city, goal_city):
        # Load and plot the map with distances
        G = self.load_map_graph_with_distances(self.romania_location_map)

        # Estimate SLDs for all cities to the goal city
        estimate_sld_to_goal_city_dict = self.estimate_sld_to_goal_city(goal_city)

        # Depth First Search
        tracemalloc.start()
        start_time = time.time()
        dfs_path = self.depth_first_search(self.map, start_city, goal_city)
        dfs_path_letters = [''.join(word[0] for word in city.split()) for city in dfs_path]
        dfs_distance = self.calculate_total_distance(dfs_path, self.map)
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("\nDepth First Search:")
        print(f"Path: {dfs_path}\nTotal Distance: {dfs_distance} km\nTime taken: {end_time - start_time:.6f} seconds")
        print(f"Current memory usage: {current / 10**6} MB; Peak memory usage: {peak / 10**6} MB")
        print(f"Path Letters: {dfs_path_letters}")
        # Plot the graph with the highlighted path and distances on edges
        self.plot_graph_with_path_and_distances(G, path=dfs_path_letters)


        # Best First Search
        tracemalloc.start()
        start_time = time.time()
        bfs_path, bfs_distance = self.best_first_search(self.map, start_city, goal_city, estimate_sld_to_goal_city_dict)
        bfs_path_letters = [''.join(word[0] for word in city.split()) for city in bfs_path]
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("\nBest First Search:")
        print(f"Path: {bfs_path}\nTotal Distance: {bfs_distance} km\nTime taken: {end_time - start_time:.6f} seconds")
        print(f"Current memory usage: {current / 10**6} MB; Peak memory usage: {peak / 10**6} MB")
        print(f"Path Letters: {bfs_path_letters}")
        # Plot the graph with the highlighted path and distances on edges
        self.plot_graph_with_path_and_distances(G, path=bfs_path_letters)


if __name__ == "__main__":
    romania_map = RomaniaMap()
    romania_map.run_searches('Arad', 'Bucharest')
