from point import Point
from grid import Grid
from wire import Wire

from extra import *

SIZE = (25,25,7)
NUMBER = 50

starts, ends = make_random_points(SIZE, resolution=2, number=NUMBER)

# Normal order, or custom order
# points_to_connect = zip(starts,ends)
points_to_connect = sort_points(starts, ends)

# Initialize the grid
points = starts+ends
mainGrid = Grid(SIZE, points)

# Start the loop for all the wires
wires = []
for start,end in points_to_connect:
    # find line, else return empty dict
    parent = mainGrid.find_line(start, end)
    if parent == {}:
        pass
    else:
        # Retrace the line and laydown the wire
        wire = mainGrid.make_wire(start, end, parent)
        con_wire = Wire(start, end, wire)
        wires.append(con_wire)
        # Update value grid
        # mainGrid.update_layer()
        mainGrid.wire_NN_edit()

# Check if wires are crossing
cross_check(wires)

# Print lenght + minimal lenght
length_score(wires)

# Plots result
mainGrid.plot_wire(wires)
