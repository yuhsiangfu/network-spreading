"""
Figure: network spreading

@auth: Yu-Hsiang Fu
@date: 2015/12/10
@update: 2018/03/22
"""
# --------------------------------------------------------------------------------
# 1.匯入套件及模組
# --------------------------------------------------------------------------------
# import modular
import matplotlib.pyplot as plt
import numpy as np

# import custom-modular
import util.handler.pickle_handler as ph

# import constant
from util.constant.constant_folder import FOLDER_IMAGE


# --------------------------------------------------------------------------------
# 2.Define variable
# --------------------------------------------------------------------------------
# simulation
NUM_SIMULATION = 100
NUM_SPREADER = 1
NUM_TIME_STEP = 50

# plot
# COLOR_LIST = ['gray', 'orange', 'y', 'b', 'c', 'm', 'r', 'k']
# MARKER_LIST = ['o', '^', 'v', '8', 'H', 's', 'D', 'x', '+']
PLOT_DPI = 300
PLOT_FORMAT = 'png'
PLOT_LAYOUT_PAD = 0.1
PLOT_X_SIZE = 4
PLOT_Y_SIZE = 4


# --------------------------------------------------------------------------------
# 3.Define function
# --------------------------------------------------------------------------------
def draw_spreading_result(net_name, spreading_result):
    for r0 in spreading_result:
        print(" --- Daw plot of r0={0}".format(r0))
        data = {}

        for measure in sorted(spreading_result[r0].keys()):
            simulation = [0] * (NUM_TIME_STEP + 1)

            for s in spreading_result[r0][measure]:
                for t in sorted(s):
                    simulation[t] += s[t]

            data[measure] = [s/NUM_SIMULATION for s in simulation]

        # --------------------------------------------------
        # create a figure
        fig, ax = plt.subplots(figsize=(PLOT_X_SIZE, PLOT_Y_SIZE), facecolor='w')

        # plot setting
        ax.grid(color="gray", linestyle="dotted", linewidth=0.5)
        ax.locator_params(axis="x", nbins=11)
        ax.set_xlim(-0.01, NUM_TIME_STEP + 1.01)
        ax.set_ylim(-0.01, 1.01)
        ax.set_xlabel('Time step', fontdict={'fontsize': 10})
        ax.set_ylabel('% infected-nodes', fontdict={'fontsize': 10})
        ax.set_xticklabels([str(round(p, 1)) for p in np.arange(0, 1.1, 0.1)])
        ax.tick_params(axis="both", direction="in", which="major", labelsize=8)

        # draw plot
        marker_index = 0
        legend_text = sorted(data)

        for measure in legend_text:
            _marker = "o"
            # _marker = MARKER_LIST[marker_index]
            # marker_index += 1
            ax.axes.plot(data[measure], linewidth=1, marker=_marker, markersize=4, markevery=1, fillstyle="none")

        # legend-text
        ax.legend(legend_text, loc=2, fontsize='medium', prop={'size': 6}, ncol=1, framealpha=0.5)

        # save image
        image_path = "{0}{1}, spreading-r0={2}-topk={3}-sim={4}-t={5}.png"
        image_path = image_path.format(FOLDER_IMAGE, net_name, r0, NUM_SPREADER, NUM_SIMULATION, NUM_TIME_STEP)
        plt.tight_layout(pad=PLOT_LAYOUT_PAD)
        plt.savefig(image_path, dpi=PLOT_DPI, format=PLOT_FORMAT)
        plt.close()


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


    # global-variable setting
    global NUM_SIMULATION, NUM_SPREADER, NUM_TIME_STEP
    NUM_SIMULATION = 100
    NUM_SPREADER = 1
    NUM_TIME_STEP = 50

    for net_name in filename_list:
        print(" - [Net] {0}:".format(net_name))
        print(" -- Read pickle file")
        file_path = "{0}{1}, spreading-topk={2}-sim={3}-t={4}.pickle"
        file_path = file_path.format(FOLDER_IMAGE, net_name, NUM_SPREADER, NUM_SIMULATION, NUM_TIME_STEP)
        spreading_result = ph.read_pickle_file(file_path)

        print(" -- Draw spreading results")
        draw_spreading_result(net_name, spreading_result)
        print(" - [/Net]\n")


if __name__ == '__main__':
    main_function()
