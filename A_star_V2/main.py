from point import Point
from grid import Grid
from wire import Wire

from extra import *
from settings import *

import time


SIZE = (17,17,7)
NUMBER = 50
LOOPS = 10

def get_wires(mainGrid, points_to_connect):
    # Start the loop for all the wires
    wires = []
    connected = 0
    wire_num = -1

    for start,end in points_to_connect:
        wire_num += 1
        # find line, else return empty dict
        parent, tries = mainGrid.find_line(start, end)
        if parent == {}:
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

    return wires, connected

if __name__ == '__main__':
    start = time.time()
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
    wires, connected = get_wires(mainGrid, points_to_connect)

    # Print lenght + minimal lenght
    total_points = len(points_to_connect)
    score = length_score(wires, connected/total_points)

    # Time!
    print('We found it in: ',time.time()-start)

    # Plots result
    mainGrid.plot_wire(wires)
