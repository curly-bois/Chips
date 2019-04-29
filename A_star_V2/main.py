from point import Point
from grid import Grid
from wire import Wire

from extra import *
from settings import *

import random

import time


SIZE = (17,17,7)
NUMBER = 50
LOOPS = 10

def get_wires(mainGrid, points_to_connect):
    # Start the loop for all the wires
    wires = []
    connected = 0
    wire_num = -1
    not_connected = []

    for start,end in points_to_connect:
        wire_num += 1
        # find line, else return empty dict
        parent, tries = mainGrid.find_line(start, end)
        if parent == {}:
            not_connected.append((start, end))
            pass
        else:
            # Retrace the line and laydown the wire
            wire = mainGrid.make_wire(start, end, parent)
            con_wire = Wire(wire_num, start, end, wire, tries)
            wires.append(con_wire)
            # Update value grid
            mainGrid.update_layer()
            # mainGrid.wire_NN_edit()
            connected += 1

    return wires, connected, not_connected

if __name__ == '__main__':
    start_time = time.time()
    # Import data
    # starts, ends = extra.make_random_points(SIZE, resolution=2, number=NUMBER)
    from data import ends, starts

    # Normal order, or custom order
    # points_to_connect = list(zip(starts,ends))
    points_to_connect = sort_points(starts, ends)
    # points_to_connect = sort_points2(starts, ends)

    # Initialize the grid
    points = starts+ends
    mainGrid = Grid(SIZE, points)

    # The hard work
    wires, connected, not_connected = get_wires(mainGrid, points_to_connect)
    old_wires = [i for i in wires]
    num_not_con = len(not_connected)

    # swap wires
    for wire in old_wires:
        not_con_len = len(not_connected)

        start, end, number = mainGrid.remove_wire(wire)
        wires2, connected2, not_connected2 = get_wires(mainGrid, not_connected)

        if not_con_len - 1 >= len(not_connected2):
            not_connected.append((start,end))
            wires += wires2
            not_connected = not_connected2
        else:
            mainGrid.add_wire(wire)

    connected = 50 - len(not_connected)
    # Print lenght + minimal lenght
    total_points = len(points_to_connect)
    score = length_score(wires, connected/total_points, not_connected)

    # Time!
    print('We found it in: ',time.time() - start_time)

    # Plots result
    mainGrid.plot_wire(wires)
