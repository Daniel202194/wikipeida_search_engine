import os
import pickle


def load_inverted_index(kind):

    path = os.getcwd() + '\\postings\\' + kind + '\\terms\\terms.txt'
    file = open(path, 'r')
    inverted_index = {}
    need_to_skip = False
    for line in file:
        if need_to_skip:
            need_to_skip = False
            continue
        split_line = line.split(',')
        try:
            inverted_index[split_line[0]] = split_line[1]
        except:
            print(split_line)
            need_to_skip = True
    return inverted_index


def save_obj(obj, name):
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
