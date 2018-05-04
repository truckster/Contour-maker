import cPickle as pickle


def pickle_safe(object, path, file_name):
    with open(path + "/" + file_name + ".pkl", 'wb') as output:
        pickle.dump(object, output, pickle.HIGHEST_PROTOCOL)