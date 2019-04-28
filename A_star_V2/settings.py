import numpy as np

layer_multiplier = [0.5,0.5,1,1.2,1.2,1.2,1.2]
# layer_multiplier = [0.4,0.7,1,1.2,1.2,1.2,1.2]
layer_coef = 0.1
z_bonus = 0.1
NN_penalty = 0.2
wire_penalty = 0.1
upper_penalty = False

def sort_points(starts, ends):
    '''
    A way of sorting the points, very easy and not thought out.
    '''
    # Make two indentical list, sort one and use the other for indexing
    distance = [abs(s[0]-e[0])+abs(s[1]-e[1]) for s,e in zip(starts,ends)]
    index = [abs(s[0]-e[0])+abs(s[1]-e[1]) for s,e in zip(starts,ends)]
    distance.sort()
    points_unsorted = list(zip(starts,ends))

    # Sort the starts and ends the same way as the distance, using the indexlist
    points = []
    for item in distance:
        i = index.index(item)
        points.append(points_unsorted[i])
        index[i] = -1

    # return the sorted points
    return points

def first_value(size):
    '''
    Very influencial defenition, creates the first instance of the value grid
    At the moment the values are set to 0, testing should result in best values
    '''
    # triple list comperhansion
    super_grid = [[[round((z)*0.00 + 0.5+
                            abs(x - 4.5) * 0.00 +
                            abs(y - 4.5) * 0.00, 2)
                            for z in range(size[2])]
                            for y in range(size[1])]
                            for x in range(size[0])]

    super_grid = [[[round(1+z*z_bonus, 2)
                            for z in range(size[2])]
                            for y in range(size[1])]
                            for x in range(size[0])]

    # Return a Numpy array (faster)
    super_matrix = np.array(super_grid)

    # layer bonus
    super_matrix *= np.array(layer_multiplier)
    return super_matrix

def update_layer(layer_info, value_grid):
    '''
    Update layers based on the info it got from the layer info
    '''
    # retrive the count dict
    empty = np.zeros(len(layer_info))

    # Calculate the occupiance of the layer
    for key in layer_info:
        layer_coverage = layer_info[key]['free']/255
        empty[key] = (1-layer_coef) + ((layer_coverage*layer_coef))

    # Matrix multiplication
    value_grid *= empty

    return value_grid

def edit_grid(grid, points, value_grid):
    '''
    Edit the value grid based on the points
    edits the values around the points and above
    '''
    # For every point
    for p in grid:
        p = grid[p]
        if p.location in points:

            # for every neighbour
            for N in p.neighbours:
                x,y,z = N.location
                value_grid[x][y][z] -= NN_penalty

            if upper_penalty:
                # for every X points above the point
                x,y,z = p.location
                for i in range(2): # This hard coded!!!!!!!!!
                    value_grid[x][y][i] -= 0.1*(3-(i+1))
    return value_grid

def wire_NN_edit(grid, value_grid):
    '''
    Edit the values of the neighbours of the wires
    '''
    # for every point
    for p in grid:
        p = grid[p]

        # If it's a wire
        if p.attribute == 'wire':

            # Set all neighbours to 0.1
            for N in p.neighbours:
                x,y,z = N.location
                value_grid[x][y][z] -= wire_penalty
    return value_grid
