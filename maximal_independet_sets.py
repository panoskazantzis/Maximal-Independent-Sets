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

    # get nodes
    nodes = list(np.unique(graph.flatten()))
    # get nodes degree
    nodes_degree = {
        nodes[i]: np.sum(adj_matrix, axis=1)[i]
        for i in range(0, len(nodes))
    }
    # get all disconnected nodes to each node
    disconnected_nodes = {
        node: np.where(adj_matrix[node] == 0)[0]
        for node in nodes
    }
    
    max_ind_sets = {}
    track_nodes = []
    while len(track_nodes) < len(nodes_degree):
        # get starting node based on priority strategy
        # prioritize
        sub_nodes_degree = {key: nodes_degree[key] for key in nodes_degree.keys() if key not in track_nodes}
        if strategy == 'min degree':
            priority_node = min(sub_nodes_degree, key=sub_nodes_degree.get)
        elif strategy == 'max degree':
            priority_node = max(sub_nodes_degree, key=sub_nodes_degree.get)
    
        # add to set - update track
        max_ind_set = [priority_node]
        max_ind_sets[priority_node] = []
        track_nodes += [priority_node]
        track_sets = []
        
        while len(max_ind_set) > 0:
            # calculate all forbiddean/connected nodes to current set
            bad_nodes = [
                node for node in nodes for in_node in max_ind_set
                if node not in disconnected_nodes[in_node] or node in max_ind_set 
                or any(
                    set(max_ind_set+[node]).issubset(set(mis[0:len(max_ind_set)+1]))
                    for mis in track_sets
                )
            ]

            # calculate all accepted/disconnected nodes to current set
            accepted_nodes = list(set(nodes) - set(bad_nodes))
            # track current set
            track_sets += [max_ind_set]
            if len(accepted_nodes) > 0:
                # add node to current set to build the MIS based on priority strategy
                sub_nodes_degree = {key: nodes_degree[key] for key in accepted_nodes}
                if strategy == 'min degree':
                    max_ind_set += [min(sub_nodes_degree, key=sub_nodes_degree.get)]
                elif strategy == 'max degree':
                    max_ind_set += [max(sub_nodes_degree, key=sub_nodes_degree.get)]
            else:
                # if subset of another MIS do not include
                if not any(
                    set(max_ind_set).issubset(set(mis)) 
                    for mis in max_ind_sets[priority_node]
                ):
                    max_ind_sets[priority_node] += [max_ind_set]
                # go 1 step back and search for other possible MIS
                max_ind_set = max_ind_set[:-1]

    # setup format - remove duplicates
    max_ind_sets = {
        tuple(sorted(tuple(mis))) for mis in list(chain.from_iterable(list(max_ind_sets.values())))
    }

    return max_ind_sets
