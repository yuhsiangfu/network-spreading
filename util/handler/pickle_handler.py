"""
Pickle file handler
@auth: Yu-Hsiang Fu
@date  2014/10/05
@update 2018/03/21
"""


def read_pickle_file(file_path):
    import pickle
    import os
    import os.path

    try:
        if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
            return pickle.load(open(file_path, 'rb'))
        else:
            raise Exception
    except:
        print('[Error] The file can not be read ...')
        print('[Error] Please check this: ' + str(file_path))


def write_pickle_file(data, file_path):
    import pickle

    try:
        pickle.dump(data, open(file_path, 'wb'))
    except:
        print('[Error] The file can not be writed ...')
        print('[Error] Please check this: ' + str(file_path))
