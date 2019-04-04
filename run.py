import connect
import grid
import load
import sys
import os
txt = os.path.join("options", sys.argv[1])

line_list = connect.main(txt)
grid_points, size = load.get_grid(txt)

grid.make_grid(grid_points, line_list, size)
