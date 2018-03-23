"""
Network spreading

@auth: Yu-Hsiang Fu
@date: 2015/12/10
@update: 2018/03/22
"""
# --------------------------------------------------------------------------------
# 1.Import modular
# --------------------------------------------------------------------------------
# import modular
# """
import numpy as np

# import custom-modular
import util.epidemic_model.sir_model as sir
import util.handler.gpickle_handler as gh
import util.handler.pickle_handler as ph

# import constant
from util.constant.constant_folder import FOLDER_FILE
from util.constant.constant_folder import FOLDER_IMAGE

# import node-attribute constant
from util.constant.constant_graph import NODE_BETWEENNESS
from util.constant.constant_graph import NODE_CLOSENESS
from util.constant.constant_graph import NODE_CLUSTERING
from util.constant.constant_graph import NODE_DEGREE
from util.constant.constant_graph import NODE_K_SHELL
from util.constant.constant_graph import NODE_PAGERANK

# import graph-attribute constant
from util.constant.constant_graph import GRAPH_THEORETICAL_THRESHOLD


# --------------------------------------------------------------------------------
# 2.Define variable
# --------------------------------------------------------------------------------
# simulation
NUM_SIMULATION = 100
NUM_SPREADER = 1
NUM_TIME_STEP = 50


# --------------------------------------------------------------------------------
# 3.Define function
# --------------------------------------------------------------------------------
def get_topk_node(g, measure, topk=1):
    node_list = [(i, round(g.node[i][measure], 4)) for i in g]
    node_list = sorted(node_list, key=lambda x: x[1], reverse=True)
    node_topk = [node_list[i][0] for i in range(0, topk)]

    return node_topk


def network_spreading(g, measure_list, r0_list):
    spreading_result = {}

    for r0 in r0_list:
        # calculate rate_recovery
        rate_infection = round(g.graph[GRAPH_THEORETICAL_THRESHOLD], 2)
        rate_recovery = round(rate_infection / r0, 2)

        # --------------------------------------------------
        print(" --- R0: {0}, b={1}, r={2}".format(r0, rate_infection, rate_recovery))
        measure_result = {}

        for measure in measure_list:
            print(" ---- Measure: {0}".format(measure))
            topk_node = get_topk_node(g, measure, topk=1)
            simulation = []

            for j in range(0, NUM_SIMULATION):
                simulation.append(sir.spreading(g, topk_node, NUM_TIME_STEP, rate_infection, rate_recovery))

            measure_result[measure] = simulation
        spreading_result[r0] = measure_result

    return spreading_result


# --------------------------------------------------------------------------------
# 4.Main function
# --------------------------------------------------------------------------------
def main_function():
    # test networks
    # filename_list = ["regular_n=1000_k=5"]
    #
    filename_list = ["ba_n=1000_k=5",
                     "random_n=1000_k=5",
                     "sw_n=1000_k=5_p=0.1"]

    # test measures
    measure_list = [NODE_BETWEENNESS,
                    NODE_CLOSENESS,
                    NODE_CLUSTERING,
                    NODE_DEGREE,
                    NODE_K_SHELL,
                    NODE_PAGERANK]

    # R0 = b/r
    r0_list = [0.5, 1.0, 1.5, 2.0]

    # global-variable setting
    global NUM_SIMULATION, NUM_SPREADER, NUM_TIME_STEP
    NUM_SIMULATION = 100
    NUM_SPREADER = 1
    NUM_TIME_STEP = 50

    for net_name in filename_list:
        print(" - [Net] {0}:".format(net_name))
        print(" -- Read gpickle file")
        file_path = "{0}{1}, analysis.gpickle".format(FOLDER_FILE, net_name)
        g = gh.read_gpickle_file(file_path)

        print(" -- Network spreading ...")
        spreading_result = network_spreading(g, measure_list, r0_list)

        print(" -- Save spreading result")
        file_path = "{0}{1}, spreading-topk={2}-sim={3}-t={4}.pickle"
        file_path = file_path.format(FOLDER_IMAGE, net_name, NUM_SPREADER, NUM_SIMULATION, NUM_TIME_STEP)
        ph.write_pickle_file(spreading_result, file_path)

        print(" - [/Net]")
        print()


if __name__ == '__main__':
    main_function()
