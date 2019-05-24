import numpy as np
import itertools
import operator
from Classes.set import Set

# this function orders all the sets according to direction and if wanted, lenghth
def dir_order(sets,mode):

    horizontal = {}
    vertical = {}
    diagonalup = {}
    diagonaldown = {}
    horlist = []
    verlist = []
    diadownlist = []
    diauplist = []

    if mode == "length":
        # sort everyting by direction
        for set in sets:
            if set.direction == "horizontal":
                horizontal[set] = set.distance
            elif set.direction == "vertical":
                vertical[set] = set.distance
            elif set.direction == "diagonal-down":
                diagonaldown[set] = set.distance
            elif set.direction == "diagonal-up":
                diagonalup[set] = set.distance

        # sort the dicts by their length and make arrays of them
        temp = sorted(diagonaldown.items(), key=operator.itemgetter(1))
        for i in temp:
            diadownlist.append(i[0])

        temp = sorted(diagonalup.items(), key=operator.itemgetter(1))
        for i in temp:
            diauplist.append(i[0])

        temp = sorted(horizontal.items(), key=operator.itemgetter(1))
        for i in temp:
            horlist.append(i[0])

        temp = sorted(vertical.items(), key=operator.itemgetter(1))
        for i in temp:
            verlist.append(i[0])

        # merge all the arrays
        complete = list(diauplist+diadownlist+verlist+horlist)

        return complete

    # only sorting by direction
    elif mode == "random":

        np.random.shuffle(sets)

        for set in sets:
            if set.direction == "horizontal":
                horlist.append(set)
            elif set.direction == "vertical":
                verlist.append(set)
            elif set.direction == "diagonal-down":
                diadownlist.append(set)
            elif set.direction == "diagonal-up":
                diauplist.append(set)

        complete = list(diauplist+diadownlist+verlist+horlist)

        return complete

# sorts the netsilst by how many times the points occur in the netlist
def appearence_order(to_be_connected):
    order = {}
    orderlist = []

    # looop through the netlist
    for set in to_be_connected:
        # if the point in a set ocurs more than 5 times, add 5 to the value to make sure these come first.
        if set.get_startpoint().get_appearence() > 4 < set.get_endpoint().get_appearence() :
                order[set] = set.get_startpoint().get_appearence() + set.get_endpoint().get_appearence() + 5
        elif set.get_startpoint().get_appearence() > 3 < set.get_endpoint().get_appearence() :
                order[set] = set.get_startpoint().get_appearence() + set.get_endpoint().get_appearence() + 3
        else:
            order[set] = set.get_startpoint().get_appearence() + set.get_endpoint().get_appearence()

    # sort
    temp = sorted(order.items(), key=operator.itemgetter(1))

    # reverse to get the most occurances first
    temp = reversed(temp)

    for i in temp:
        orderlist.append(i[0])
    return orderlist
