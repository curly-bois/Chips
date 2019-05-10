import connect
import grid
import load
import sys
import os

# Fetchs the system variables
if len(sys.argv) < 2:
    print()
    sys.exit(1)

# Parse
txt = os.path.join("options", sys.argv[1])

# Excecute programs
line_list = connect.main(txt)
grid_points, size = load.get_grid(txt)

# Plot results
grid.make_grid(grid_points, line_list, size)
