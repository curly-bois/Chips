import numpy as np
import itertools
from Classes.set import Set

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
        for set in sets:
            if set.direction == "horizontal":
                horizontal[set] = set.distance
            elif set.direction == "vertical":
                vertical[set] = set.distance
            elif set.direction == "diagonal-down":
                diagonaldown[set] = set.distance
            elif set.direction == "diagonal-up":
                diagonalup[set] = set.distance

        temp = sorted(diagonaldown.items(), key=operator.itemgetter(1))
        temp = reversed(temp)
        for i in temp:
            diadownlist.append(i[0])

        temp = sorted(diagonalup.items(), key=operator.itemgetter(1))
        # temp = reversed(temp)
        for i in temp:
            diauplist.append(i[0])

        temp = sorted(horizontal.items(), key=operator.itemgetter(1))
        # temp = reversed(temp)
        for i in temp:
            horlist.append(i[0])

        temp = sorted(vertical.items(), key=operator.itemgetter(1))
        # temp = reversed(temp)
        for i in temp:
            verlist.append(i[0])

        complete = list(diauplist+diadownlist+verlist+horlist)

        return complete

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


def appearence_order(to_be_connected):
    order = {}
    orderlist = []

    for set in to_be_connected:
        if set.get_startpoint().get_appearence() > 3 < set.get_endpoint().get_appearence() :
            order[set] = set.get_startpoint().get_appearence() + set.get_endpoint().get_appearence() + 3
        else:
            order[set] = set.get_startpoint().get_appearence() + set.get_endpoint().get_appearence()

    temp = sorted(order.items(), key=operator.itemgetter(1))
    temp = reversed(temp)

    for i in temp:
        orderlist.append(i[0])
    return orderlist
