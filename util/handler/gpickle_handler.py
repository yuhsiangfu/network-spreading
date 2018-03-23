"""
Gpickle file handler
@auth: Yu-Hsiang Fu
@date  2014/09/28
@update 2018/03/22
"""


def read_gpickle_file(file_path):
    import networkx as nx
    import os
    import os.path

    try:
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            return nx.read_gpickle(file_path)
        else:
            raise Exception
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this: ' + str(file_path))


def write_gpickle_file(G, file_path):
    import networkx as nx

    try:
        nx.write_gpickle(G, file_path)
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this: ' + str(file_path))
