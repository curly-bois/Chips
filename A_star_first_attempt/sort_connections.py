from init_2 import *

import operator
import numpy

connections = get_connections()
matrix = matrix(get_grid())
print("in de sort_connections")
to_be_connected = make_conlist(connections,matrix)

to_be_sorted = {}

def calculate_difference(start, end):
    manhattan_difference = 0
    difference = numpy.subtract(start, end)
    for dimensional_difference in difference:
        manhattan_difference += abs(dimensional_difference)

    return manhattan_difference

def sort_list():

    for connection in to_be_connected:
        start = connection[0].get_location()
        end = connection[1].get_location()
        difference = calculate_difference(start, end)
        print(difference)
        print(connection)
        to_be_sorted[tuple(connection)] = difference

    sorted_connections = sorted(to_be_sorted.items(), key = operator.itemgetter(1))

    sorted_list = []

    for connection in sorted_connections:
        sorted_list.append(connection[0])

    print(sorted_list)
    return(sorted_list)

sort_list()
