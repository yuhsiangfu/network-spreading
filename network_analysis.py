"""
Network attribute analysis

@auth: Yu-Hsiang Fu
@date: 2014/12/10
@update: 2018/03/22
"""
# --------------------------------------------------------------------------------
# 1.Import modular
# --------------------------------------------------------------------------------
# import modular
import math
import networkx as nx
import numpy as np
import warnings

# import custom-modular
import util.handler.edgelist_handler as eh
import util.handler.gpickle_handler as gh

# import constant
from util.constant.constant_folder import FOLDER_EDGELIST
from util.constant.constant_folder import FOLDER_FILE

# import node-attribute constant
from util.constant.constant_graph import NODE_BETWEENNESS
from util.constant.constant_graph import NODE_CLOSENESS
from util.constant.constant_graph import NODE_CLUSTERING
from util.constant.constant_graph import NODE_DEGREE
from util.constant.constant_graph import NODE_K_SHELL
from util.constant.constant_graph import NODE_PAGERANK

# import graph-attribute constant
from util.constant.constant_graph import GRAPH_DEGREE_ASSORTATIVITY
from util.constant.constant_graph import GRAPH_AVG_DEGREE
from util.constant.constant_graph import GRAPH_AVG_DEGREE_SQUARE
from util.constant.constant_graph import GRAPH_DEGREE_HETEROGENEITY
from util.constant.constant_graph import GRAPH_THEORETICAL_THRESHOLD


# --------------------------------------------------------------------------------
# 2.Define function
# --------------------------------------------------------------------------------
def create_network(edge_list):
    g = nx.parse_edgelist(edge_list, nodetype=int)
    g = g.to_undirected()
    g.remove_edges_from(g.selfloop_edges())

    return g


def compute_attributes(g):
    print(" -- Nodes' attributes")
    print(" --- Betweenness")
    node_betweenness = nx.betweenness_centrality(g)

    print(" --- Closeness")
    node_closeness = nx.closeness_centrality(g)

    print(" --- Clustering")
    node_clustering = nx.clustering(g)

    print(" --- Degree")
    node_degree = nx.degree(g)

    print(" --- K-core")
    node_kshell = nx.core_number(g)

    print(" --- PageRank")
    node_pagerank = nx.pagerank(g, alpha=0.85, max_iter=150)

    # add attributes to nodes
    for i in g:
        g.node[i][NODE_BETWEENNESS] = node_betweenness[i]
        g.node[i][NODE_CLOSENESS] = node_closeness[i]
        g.node[i][NODE_CLUSTERING] = node_clustering[i]
        g.node[i][NODE_DEGREE] = node_degree[i]
        g.node[i][NODE_K_SHELL] = node_kshell[i]
        g.node[i][NODE_PAGERANK] = node_pagerank[i]

    # --------------------------------------------------
    print(" -- Graph attributes")
    print(" --- Degree-assortativity")
    with warnings.catch_warnings():
        warnings.filterwarnings('error')

        try:
            g.graph[GRAPH_DEGREE_ASSORTATIVITY] = nx.degree_assortativity_coefficient(g)
        except RuntimeWarning:
            g.graph[GRAPH_DEGREE_ASSORTATIVITY] = 0

    print(" --- Degree-heterogeneity")
    g.graph[GRAPH_AVG_DEGREE] = np.mean([g.node[i][NODE_DEGREE] for i in g])
    g.graph[GRAPH_AVG_DEGREE_SQUARE] = np.mean([pow(g.node[i][NODE_DEGREE], 2) for i in g])
    g.graph[GRAPH_DEGREE_HETEROGENEITY] = g.graph[GRAPH_AVG_DEGREE_SQUARE] / pow(g.graph[GRAPH_AVG_DEGREE], 2)
    g.graph[GRAPH_THEORETICAL_THRESHOLD] = g.graph[GRAPH_AVG_DEGREE] / g.graph[GRAPH_AVG_DEGREE_SQUARE]

    return g


# --------------------------------------------------------------------------------
# 3.Main function
# --------------------------------------------------------------------------------
def main_function():
    # test networks
    # filename_list = ["regular_n=1000_k=5"]
    filename_list = ["ba_n=1000_k=5",
                     "random_n=1000_k=5",
                     "regular_n=1000_k=5",
                     "sw_n=1000_k=5_p=0.1"]

    for net_name in filename_list:
        print(" - [Net] {0}:".format(net_name))
        print("  - Create a network")
        file_path = "{0}{1}.txt".format(FOLDER_EDGELIST, net_name)
        g = create_network(eh.read_edgelist(file_path))

        print("  - Compute attributes")
        g = compute_attributes(g)

        # Save gpickle file
        print("  - Save gpickle file")
        file_path = "{0}{1}, analysis.gpickle".format(FOLDER_FILE, net_name)
        gh.write_gpickle_file(g, file_path)
        print(" - [/Net]")


if __name__ == '__main__':
    main_function()
