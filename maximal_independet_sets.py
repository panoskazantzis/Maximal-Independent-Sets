# Maximal Independent Sets in graphs

import pandas as pd
import numpy as np
from itertools import chain


def get_adjacency_matrix(graph, nodes):
    """
    Compute the adjacency matrix of given graph.

    Takes as input a graph in np.array format containing the edges of a graph and
    computes the adjacency matrix.

    Assumes each node is connected to itself.

    Parameters
    ----------
    graph : np.array
        np.array representing the edges of a graph.
    nodes : list
        The labels of the nodes of the graph.

    Returns
    -------
    adj_mtrx : np.array
        np.array representing the adjacency matrix of the graph.
    """
    # initialize adjacency matrix
    adj_mtrx = np.array([[0]*len(nodes)]*len(nodes))
    
    # compute adjacency matrix
    for i_edge in range(len(graph)):
        node_start = np.where(nodes == graph[i_edge][0])[0][0]
        node_end = np.where(nodes == graph[i_edge][1])[0][0]
        adj_mtrx[node_start, node_end] = 1
        adj_mtrx[node_end, node_start] = 1
    
    # assume each node is connected to itself
    for i in range(len(adj_mtrx)):
        adj_mtrx[i, i] = 1
        
    return adj_mtrx
