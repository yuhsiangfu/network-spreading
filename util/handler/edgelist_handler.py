"""
Edgelist handler

@auth: Yu-Hsiang Fu
@date: 2014/09/27
@update 2018/03/21
"""


def read_edgelist(file_path):
    import os
    import os.path

    edge_list = []

    try:
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            with open(file_path, mode="r") as f:
                for line in f:
                    edge_list.append(line.strip())
                f.close()
        else:
            raise Exception
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this file:  ' + str(file_path))
    return edge_list



def write_edgelist(G, file_path):
    import networkx as nx

    try:
        nx.write_edgelist(G, path=file_path, data=False)
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this file:  ' + str(file_path))
