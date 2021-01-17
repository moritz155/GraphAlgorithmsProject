# GraphAlgorithmsProject

This code gets a csv file with an adjacency list from a planar graph as input. Example graphs in csv format are given. 
The algorithm applies a four coloring to this graph, looks for further coloring possibilities and then finds the best combination of each two colors that can be grouped together so that the number of faces in the new graph is minimal. The output is a four coloring of the graph and a recommendation of colors one should group together to minimize the faces. When grouping the colors together one gets a bipartite graph. 
