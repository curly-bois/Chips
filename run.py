import connect
import grid
import load


txt = r"list_1.txt"

line_list = connect.main(txt)
grid_points, size = load.get_grid(txt)

grid.make_grid(grid_points, line_list, size)
