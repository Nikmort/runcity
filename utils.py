import pickle

def print_regions(regions):
    for region in regions:
        print('{}\n***{}***'.format(20 * '=', region))
        print_streets(regions[region])


def print_streets(streets):
    for street in streets:
        print(', '.join(street))
        print_houses(streets[street])


def print_houses(houses):
    to_print = []
    for house in houses:
        to_print.append(house['ft'])
    print(', '.join(to_print))


def save_obj(obj, filename):
    with open(filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(filename):
    with open(filename + '.pkl', 'rb') as f:
        return pickle.load(f)
