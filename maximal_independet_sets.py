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


def maximal_independent_sets(graph, strategy='min degree'):
    # calculate adjacency matrix
    adj_matrix = get_adjacency_matrix(graph, np.unique(graph.flatten()))
    # find 1st independent maximal set
    
    
    max_ind_sets = []
    
    # get nodes degree
    track_nodes = list(np.unique(graph.flatten()))
    nodes_degree = {
        track_nodes[i]: np.sum(adj_matrix, axis=1)[i]
        for i in range(0, len(track_nodes))
    }
    # get all disconnected nodes to each node
    disconnected_nodes = {
        node: np.where(adj_matrix[node] == 0)[0]
        for node in track_nodes
    }
    
    max_ind_sets = {}
    while len(nodes_degree) > 0:
    
        # prioritize
        if strategy == 'min degree':
            priority_node = min(nodes_degree, key=nodes_degree.get)
        elif strategy == 'max degree':
            priority_node = max(nodes_degree, key=nodes_degree.get)
    
        # add to set
        max_ind_set = [priority_node]
        max_ind_sets[priority_node] = []
        
        
        while len(max_ind_set) > 0:
            #print(max_ind_set)
            #
            # get all accepted nodes
            bad_nodes = [
                node for node in set(np.unique(graph.flatten()))
                for in_node in max_ind_set
                if node not in disconnected_nodes[in_node] or node in set(max_ind_set) 
                or any(set(max_ind_set+[node]).issubset(set(mis)) for mis in max_ind_sets[priority_node])
                #or max_ind_set+[node] in max_ind_sets
            ]

            accepted_nodes = set(np.unique(graph.flatten())) - set(bad_nodes)
            if len(accepted_nodes) > 0:
                max_ind_set += [list(accepted_nodes)[0]]
            else:
                # if subset do not include
                if not any(set(max_ind_set).issubset(set(mis)) for mis in max_ind_sets[priority_node]):
                    max_ind_sets[priority_node] += [max_ind_set]
                max_ind_set = max_ind_set[:-1]
            
        # next starting node
        nodes_degree = {item[0]: item[1] for item in nodes_degree.items() if item[0] != priority_node}
    
    max_ind_sets = [
        list(set(mis)) for mis in list(chain.from_iterable(list(max_ind_sets.values())))
    ]
    
    return list(set(map(tuple, max_ind_sets)))
