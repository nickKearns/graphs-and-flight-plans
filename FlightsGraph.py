from collections import deque


class AirportVertex(object):
    
    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.id = vertex_id
        self.neighbors_dict = {} # id -> (obj, weight)

    def add_neighbor(self, vertex_obj, weight):
        """
        Add a neighbor by storing it in the neighbors dictionary.
        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        weight (number): The weight of this edge.
        """
        if vertex_obj.get_id() in self.neighbors_dict.keys():
            return # it's already a neighbor

        self.neighbors_dict[vertex_obj.get_id()] = (vertex_obj, weight)

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return [neighbor for (neighbor, weight) in self.neighbors_dict.values()]

    def get_neighbors_with_weights(self):
        """Return the neighbors of this vertex."""
        return list(self.neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.id

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        # neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        # return f'{self.id} adjacent to {neighbor_ids}'
        return self.get_id()

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = [neighbor.get_id() for neighbor in self.get_neighbors()]
        return f'{self.id} adjacent to {neighbor_ids}'






class FlightsGraph(object):

    INFINITY = float('inf')

    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.
        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.vertex_dict = {}
        self.is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.
        Returns:
        Vertex: The new vertex object.
        """
        if vertex_id in self.vertex_dict.keys():
            return False # it's already there
        vertex_obj = AirportVertex(vertex_id)
        self.vertex_dict[vertex_id] = vertex_obj
        return True

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.vertex_dict.keys():
            return None
        vertex_obj = self.vertex_dict[vertex_id]
        return vertex_obj
    
    def add_edge(self, vertex_id1, vertex_id2, weight):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.
        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        weight (number): The edge weight.
        """
        all_ids = self.vertex_dict.keys()
        if vertex_id1 not in all_ids or vertex_id2 not in all_ids:
            return False
        vertex_obj1 = self.get_vertex(vertex_id1)
        vertex_obj2 = self.get_vertex(vertex_id2)
        vertex_obj1.add_neighbor(vertex_obj2, weight)
        if not self.is_directed:
            vertex_obj2.add_neighbor(vertex_obj1, weight)

    def get_vertices(self):
        """Return all the vertices in the graph"""
        return list(self.vertex_dict.values())

    def __iter__(self):
        """Iterate over the vertex objects in the graph, to use sytax:
        for vertex in graph"""
        return iter(self.vertex_dict.values())

    def union(self, parent_map, vertex_id1, vertex_id2):
        """Combine vertex_id1 and vertex_id2 into the same group."""
        vertex1_root = self.find(parent_map, vertex_id1)
        vertex2_root = self.find(parent_map, vertex_id2)
        parent_map[vertex1_root] = vertex2_root


    def find(self, parent_map, vertex_id):
        """Get the root (or, group label) for vertex_id."""
        if(parent_map[vertex_id] == vertex_id):
            return vertex_id
        return self.find(parent_map, parent_map[vertex_id])





    def minimum_spanning_tree_kruskal(self):
        """
        Use Kruskal's Algorithm to return a list of edges, as tuples of 
        (start_id, dest_id, weight) in the graph's minimum spanning tree.
        """
        # TODO: Create a list of all edges in the graph, sort them by weight 
        # from smallest to largest
        
        vertices_checked_for_weights = set()
        weights = []


        for vertex_id in self.vertex_dict:
            vertex_obj = self.get_vertex(vertex_id)
            for neighbor, weight in vertex_obj.get_neighbors_with_weights():
                neighbor_id = neighbor.get_id()
                weights.append((weight, vertex_id, neighbor_id))
                    
            vertices_checked_for_weights.add(neighbor)
        weights = sorted(weights)
        # return weights


        # TODO: Create a dictionary `parent_map` to map vertex -> its "parent". 
        # Initialize it so that each vertex is its own parent.

        parent_map = {}
        for vertex_id in self.vertex_dict:
            parent_map[vertex_id] = vertex_id
        


        # TODO: Create an empty list to hold the solution (i.e. all edges in the 
        # final spanning tree)

        solution_list = []

        # TODO: While the spanning tree holds < V-1 edges, get the smallest 
        # edge. If the two vertices connected by the edge are in different sets 
        # (i.e. calling `find()` gets two different roots), then it will not 
        # create a cycle, so add it to the solution set and call `union()` on 
        # the two vertices.


        while len(solution_list) < len(self.vertex_dict) - 1:
            current_smallest_weight, vertex_one_id, vertex_two_id = weights.pop(0)
            if self.find(parent_map, vertex_one_id) != self.find(parent_map, vertex_two_id):
                mst_edge = (vertex_one_id, vertex_two_id, current_smallest_weight)
                solution_list.append(mst_edge)
                self.union(parent_map, vertex_one_id, vertex_two_id)

        return solution_list




    def find_shortest_path(self, start_id, target_id):
        """
        Use Dijkstra's Algorithm to return the total weight of the shortest path
        from a start vertex to a destination.
        """
        # TODO: Create a dictionary `vertex_to_distance` and initialize all
        # vertices to INFINITY - hint: use `float('inf')`


        vertex_to_distance = {}

        for vertex in self.vertex_dict:
            if vertex == start_id:
                vertex_to_distance[vertex] = 0
            else:
                vertex_to_distance[vertex] = float('inf')


        # TODO: While `vertex_to_distance` is not empty:
        # 1. Get the minimum-distance remaining vertex, remove it from the
        #    dictionary. If it is the target vertex, return its distance.
        # 2. Update that vertex's neighbors by adding the edge weight to the
        #    vertex's distance, if it is lower than previous.

        while vertex_to_distance:

            current_shortest_edge = float('inf')
            current_vertex_id = None
            #find the current shortest distance from the start vertex
            for vertex_id in vertex_to_distance:
                weight = vertex_to_distance[vertex_id]
                if weight < current_shortest_edge:
                    current_lowest = weight
                    current_vertex_id = vertex_id

            if current_vertex_id == target_id:
                return vertex_to_distance[current_vertex_id]

            
            current_vertex_obj = self.get_vertex(current_vertex_id)


            for neighbor, weight in current_vertex_obj.get_neighbors_with_weights():
                neighbor_id = neighbor.get_id()
                if neighbor_id in vertex_to_distance:
                    vertex_to_distance[neighbor_id] = min(weight + vertex_to_distance[current_vertex_id], vertex_to_distance[neighbor_id])

            # print(vertex_to_distance)

            vertex_to_distance.__delitem__(current_vertex_id)
        
    def floyd_warshall(self):
        """
        Return the All-Pairs-Shortest-Paths dictionary, containing the shortest
        paths from each vertex to each other vertex.
        """

        dist = dict()

        all_vertex_ids = self.vertex_dict.keys()

        for vertex1 in all_vertex_ids:
            dist[vertex1] = dict()
            for vertex2 in all_vertex_ids:
                dist[vertex1][vertex2] = FlightsGraph.INFINITY
            dist[vertex1][vertex1] = 0


        all_vertex_objs = self.get_vertices()

        for vertex in all_vertex_objs:
            neighbors_with_weights = vertex.get_neighbors_with_weights()

            for neighbor, weight in neighbors_with_weights:
                dist[vertex.get_id()][neighbor.get_id()] = weight




        for k in self.vertex_dict.keys():
            for i in self.vertex_dict.keys():
                for j in self.vertex_dict.keys():
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        return dist


    def fillOrder(self,vertex,visited, stack): 
        visited.add(vertex)

        for neighbor in vertex.get_neighbors(): 
            if neighbor not in visited: 
                self.fillOrder(neighbor, visited, stack) 
        stack = stack.append(vertex) 


    def transpose_graph(self):
        '''
        This function will reverse the direction of the edges in a graph
        to find the transpose of the graph
        '''

        graph_copy = self

        for vertex1 in self.get_vertices():
            for vertex2 in vertex1.get_neighbors():
                graph_copy.add_edge(vertex2.get_id(), vertex1.get_id(), 0)

        return graph_copy



    def dfs_traversal_recursive(self, vertex, visited_vertices):
        scc_group = []
        scc_group.append(vertex)
        visited_vertices.add(vertex)
        
        for neighbor in vertex.get_neighbors():
            if neighbor not in visited_vertices:
                self.dfs_traversal_recursive(neighbor, visited_vertices)
        return scc_group

    def kosaraju_find_SCC(self):
        '''
        Use kosaraju's algorithm to find the strongly connected components
        in a directed graph. This algorithm does not take into account the weights
        because the weights do not change whether a group of vertices are strongly connected or 
        not
        '''

        stack = deque()

        visited_vertices = set()

        for vertex in self.get_vertices():
            if vertex not in visited_vertices:
                self.fillOrder(vertex, visited_vertices, stack)

        transposed_graph = self.transpose_graph()

        visited_vertices.clear()

        while stack:
            last_vertex = stack.pop()
            current_scc_group = []
            if last_vertex not in visited_vertices:
                current_scc_group = transposed_graph.dfs_traversal_recursive(last_vertex, visited_vertices)
        print('')
        