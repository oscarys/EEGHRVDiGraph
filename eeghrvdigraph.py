import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class EEGHRVDiGraph():
    """Class to handle EEG-HRV digraphs"""
    # Compute position on unit circle from ccw index (inx) from P4
    EEGHRVpos = lambda inx: [np.cos(2*np.pi*inx/14), np.sin(2*np.pi*inx/14)]
    # Define colors to draw left (lh), right(rh) hemisphere, central ('cl') or 'hrv' nodes, 
    EEGHRVcol = {'lh': [1.0, 0.4, 0.4, 1.0], 'rh': [0.6, 1.0, 0.6, 1.0], 'cl': [0.6, 1.0, 1.0, 1.0], 
                 'hrv': [0.8, 0.8, 0.0, 1.0], 'edge': [0.6, 0.6, 0.6, 0.3]}    
    # EEG-HRV graph list of node dictionaries
    EEGHRVnodes = [('Fp1', {'loc': EEGHRVpos( 4), 'c': EEGHRVcol['lh']}), 
                   ('Fp2', {'loc': EEGHRVpos( 3), 'c': EEGHRVcol['rh']}), 
                   ( 'F3', {'loc': EEGHRVpos( 5), 'c': EEGHRVcol['lh']}), 
                   ( 'Fz', {'loc': EEGHRVpos( 9), 'c': EEGHRVcol['cl']}), 
                   ( 'F4', {'loc': EEGHRVpos( 2), 'c': EEGHRVcol['rh']}), 
                   ( 'C3', {'loc': EEGHRVpos( 6), 'c': EEGHRVcol['lh']}), 
                   ( 'Cz', {'loc': EEGHRVpos(10), 'c': EEGHRVcol['cl']}), 
                   ( 'C4', {'loc': EEGHRVpos( 1), 'c': EEGHRVcol['rh']}), 
                   ( 'P3', {'loc': EEGHRVpos( 7), 'c': EEGHRVcol['lh']}), 
                   ( 'Pz', {'loc': EEGHRVpos(11), 'c': EEGHRVcol['cl']}),
                   ( 'P4', {'loc': EEGHRVpos( 0), 'c': EEGHRVcol['rh']}), 
                   ( 'O1', {'loc': EEGHRVpos( 8), 'c': EEGHRVcol['lh']}), 
                   ( 'Oz', {'loc': EEGHRVpos(12), 'c': EEGHRVcol['cl']}), 
                   ( 'O2', {'loc': EEGHRVpos(13), 'c': EEGHRVcol['rh']}), 
                   ('HRV', {'loc':    (0.0, 0.0), 'c': EEGHRVcol['hrv']})]
    
    def __init__(self, adjacency=None, edges=None):
        """Constructor from an adjacency matrix from Pandas"""
        # New Digraph
        self.graph = nx.DiGraph()
        # Add nodes from lod
        self.graph.add_nodes_from(self.EEGHRVnodes)
        # If building from adjacency matrix
        if adjacency is not None:
            # Parse each row of adjacency matrix to build edges
            for node in range(adjacency.shape[0]):
                edges = [(self.EEGHRVnodes[node][0], self.EEGHRVnodes[i][0]) 
                         for i, v in enumerate(adjacency.iloc[node,:]) if v==1.0]
                # Add edges for this row
                self.graph.add_edges_from(edges)
        # If building from edges
        elif edges is not None:
            self.graph.add_edges_from(edges)
        else:
            del self
        
    def __str__(self):
        """Repeat nx.Digraph __str__"""
        return '{}'.format(self.graph)
    
    def draw(self, axes, title='', fontsize=20):
        """Plot the EEG-HRV graph"""
        nx.draw(self.graph, pos={node: self.graph.nodes[node]['loc'] for node in self.graph.nodes},
                ax=axes, labels={node: node for node in self.graph.nodes}, font_size= 10,
                node_color=[self.graph.nodes[node]['c'] for node in self.graph.nodes], node_size=600,
                edge_color=[self.EEGHRVcol['hrv'] if 'HRV' in edge else self.EEGHRVcol['edge'] 
                            for edge in self.graph.edges])
        # Set title
        axes.text(0.9, 0.9, title, fontsize=fontsize);
        
    def nonNeighbors(self, node1, node2):
        """Build subtree of nodes not mutually neighbors to node1 and node2"""
        # Check if node1 and node2 are connected bidirectionally
        if (node1, node2) in self.graph.edges and (node2, node1) in self.graph.edges:
            # Get the set of breadth-first tree edges from both nodes
            bft_node1 = nx.bfs_tree(self.graph, node1).edges
            bft_node2 = nx.bfs_tree(self.graph, node2).edges
            # Search for nodes at distance 1 of node1 or node2 but not both
            edges = set()
            for edge in bft_node1:
                if edge[0] == node1 and (node2, edge[1]) not in bft_node2:
                    edges.add(edge)
            for edge in bft_node2:
                if edge[0] == node2 and (node1, edge[1]) not in bft_node1:
                    edges.add(edge)
            return EEGHRVDiGraph(edges=edges)
        else:
            return EEGHRVDiGraph()

