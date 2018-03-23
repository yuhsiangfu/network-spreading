"""
Theoretical network generator

@auth: Yu-Hsiang Fu
@date: 2013/11/17
@update: 2018/03/21
"""
# --------------------------------------------------------------------------------
# 1.Import packages
# --------------------------------------------------------------------------------
# import modular
import networkx as nx

# import custom-modular
import util.handler.edgelist_handler as eh

# import constant
from util.constant.constant_folder import FOLDER_EDGELIST


# --------------------------------------------------------------------------------
# 2.Define variables
# --------------------------------------------------------------------------------
NUMBER_NODES = 1000
NUMBER_DEGREE = 5
PROBABILITY_REWIRE = 0.1


# --------------------------------------------------------------------------------
# 3.Main function
# --------------------------------------------------------------------------------
def main_function():
    print("Generate regular network.")
    # p=0 in small-world model is regular network
    g = nx.watts_strogatz_graph(NUMBER_NODES, NUMBER_DEGREE, 0)
    g.remove_edges_from(g.selfloop_edges())
    g.to_undirected()
    file_name = "{0}regular_n={1}_k={2}.txt".format(FOLDER_EDGELIST, NUMBER_NODES, NUMBER_DEGREE)
    eh.write_edgelist(g, file_name)

    # --------------------------------------------------
    print("Generate random network.")
    # random: p=1 is random network
    g = nx.watts_strogatz_graph(NUMBER_NODES, NUMBER_DEGREE, 1)
    g.remove_edges_from(g.selfloop_edges())
    g.to_undirected()
    file_name = "{0}random_n={1}_k={2}.txt".format(FOLDER_EDGELIST, NUMBER_NODES, NUMBER_DEGREE)
    eh.write_edgelist(g, file_name)

    # --------------------------------------------------
    print("Generate small-world network.")
    # small-world
    g = nx.watts_strogatz_graph(NUMBER_NODES, NUMBER_DEGREE, PROBABILITY_REWIRE)
    g.remove_edges_from(g.selfloop_edges())
    g.to_undirected()
    file_name = "{0}sw_n={1}_k={2}_p={3}.txt".format(FOLDER_EDGELIST, NUMBER_NODES, NUMBER_DEGREE, PROBABILITY_REWIRE)
    eh.write_edgelist(g, file_name)

    # --------------------------------------------------
    print('Generate scale-free network.')
    # scale-free network: power-law
    g = nx.barabasi_albert_graph(NUMBER_NODES, NUMBER_DEGREE)
    g.remove_edges_from(g.selfloop_edges())
    g.to_undirected()
    file_name = "{0}ba_n={1}_k={2}.txt".format(FOLDER_EDGELIST, NUMBER_NODES, NUMBER_DEGREE)
    eh.write_edgelist(g, file_name)


if __name__ == '__main__':
    main_function()
