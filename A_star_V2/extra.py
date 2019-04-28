import random
import numpy as np

def cal_val(value_grid, tup_cur, tup_end, tup_start):
    '''
    Calculate the values for the Astar Algo
    '''
    # Get distance values
    dis2end = threedimdistance(tup_cur, tup_end)
    dis2start = threedimdistance(tup_start, tup_cur)

    # Get coordinates
    x,y,z = tup_cur[0],tup_cur[1],tup_cur[2]

    # Adjust for value_grid
    value = ( dis2end - dis2start)*float(value_grid[x][y][z])
    return value

def threedimdistance( i, j):
    '''
    Get three dimesional distance
    '''
    deltaxsquared = (i[0] - j[0]) ** 2
    deltaysquared = (i[1] - j[1]) ** 2
    deltazsquared = (i[2] - j[2]) ** 2
    return (deltaxsquared + deltaysquared + deltazsquared) ** 0.5

def make_random_points(size, resolution, number=-1):
    '''
    FOR TESTING, make some random points
    can be used to find optimal values
    '''
    points = []
    # Make random points
    for i in range(0,size[0],resolution):
        for j in range(0,size[1],resolution):
            points.append((i,j,0))

    # Remove uneven points
    if len(points) % 2 != 0:
        points = points[:-1]

    # shuffle, cut and divide in start en end
    random.shuffle(points)
    points = points[:number]
    ends = points[int(len(points)/2):]
    starts = points[:int(len(points)/2)]

    return starts, ends

def cross_check(wires):
    '''
    Checks if a line is crossing (For testing)
    '''
    all = []
    for w in wires:
        all += w.route

    print('\nNothing is crossing =', end='')
    print(len(all) == len(set(all)), '\n')

def check_duplicates(points, count):
    '''
    Checks if a point is dubble (for testing)
    '''
    print("No duplicates =", end='')
    print(len(points) == count )

def length_score(wires, percentile):
    '''
    Nice start of how we can "SCORE" our result
    (Store in CSV????)
    '''
    # Retrive data
    len_list = [len(i.route) for i in wires]
    minlen_list = [abs(i.start[0] - i.end[0]) +
                   abs(i.start[1] - i.end[1])
                   for i in wires]

    # Stats
    true_len = sum(len_list)
    longest = max(len_list)
    shortest = min(len_list)
    mean = true_len / len(len_list)

    # Boundaries
    min_len = sum(minlen_list)
    Mlongest = max(minlen_list)
    Mshortest = min(minlen_list)
    Mmean = min_len / len(minlen_list)

    # Print all
    print('-------------------')
    print('Summary of the Routes')
    print('Total lenght: %.3f' % true_len)
    print('Longest: %.3f' % longest)
    print('Shortest: %.3f' % shortest)
    print('Mean: %.3f' % mean)
    print('percentile connected: %.3f' % percentile)
    print('-------------------')
    print('Summary of the Boundaries')
    print('Minimal Length: %.3f' % min_len)
    print('Minimal Longest: %.3f' % Mlongest)
    print('Minimal shortest: %.3f' % Mshortest)
    print('Minimal mean: %.3f' % Mmean)
    print('-------------------')

    return percentile

def make_imported_points(points, netlist):
    start_index, end_index = zip(*netlist)
    starts = [(points[i][0],points[i][1],0) for i in start_index]
    ends = [(points[i][0],points[i][1],0) for i in end_index]
    return ends, starts
