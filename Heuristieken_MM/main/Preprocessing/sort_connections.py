from init import *

import operator
import numpy

def calculate_difference(start, end):
    manhattan_difference = 0
    difference = numpy.subtract(start, end)
    for dimensional_difference in difference:
        manhattan_difference += abs(dimensional_difference)

    return manhattan_difference

def sort_list(to_be_connected):
    to_be_sorted = {}
    for set in to_be_connected:
        start = set.get_startpoint().get_location()
        end = set.get_endpoint().get_location()
        difference = calculate_difference(start, end)
        to_be_sorted[set] = difference

    sorted_connections = sorted(to_be_sorted.items(), key = operator.itemgetter(1))

    sorted_list = []

    for connection in sorted_connections:
        sorted_list.append(connection[0])

    return(list(reversed(sorted_list)))
