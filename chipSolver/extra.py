from point import Point
from wire import Wire

import random
import numpy as np
import pandas as pd
import sys
import time

def get_wires(mainGrid, points_to_connect):
    # Start the loop for all the wires
    wires = []
    connected = 0
    not_connected = []

    for start,end in points_to_connect:
        # find line, else return empty dict
        parent = mainGrid.Astar(start, end)
        if parent == {}:
            not_connected.append((start, end))
            pass
        else:
            # Retrace the line and laydown the wire
            wire = mainGrid.make_wire(start, end, parent)
            con_wire = Wire(start, end, wire)
            wires.append(con_wire)
            # Update value grid
            mainGrid.update_layer()
            # mainGrid.wire_NN_edit() ## Commented out
            connected += 1

    return wires, connected, not_connected

def swap_wires(wires, not_connected, mainGrid, swaps):

    old_wires = [i for i in wires]
    random.shuffle(old_wires)

    # len_list = sum([len(i.route) for i in wires])
    len_list = len(not_connected)
    not_connected_new = []
    for wire in old_wires[:swaps]:
        start, end = mainGrid.remove_wire(wire)
        not_connected_new.append((start, end))
        not_con_len = len(not_connected)

    points_to_connect = not_connected+not_connected_new
    random.shuffle(points_to_connect)
    wires2, connected, not_connected2 = get_wires(mainGrid, points_to_connect)
    # len_list2 = sum([len(i.route) for i in wires2 + old_wires[3:]])
    len_list2 = len(not_connected2)

    if len_list > len_list2:
        wires = wires2 + old_wires[swaps:]
        not_connected = not_connected2
    else:
        for w in wires2:
            mainGrid.remove_wire(w)
        for w in old_wires[swaps:]:
            mainGrid.add_wire(w)

    random.shuffle(not_connected)
    return mainGrid, wires, not_connected

def swap_wires_for_score(wires, not_connected, mainGrid, swaps):

    old_wires = [i for i in wires]
    random.shuffle(old_wires)

    len_list = sum([len(i.route) for i in wires])
    len1 = len(not_connected)
    not_connected_new = []
    for wire in old_wires[:swaps]:
        start, end = mainGrid.remove_wire(wire)
        not_connected_new.append((start, end))
        not_con_len = len(not_connected)

    points_to_connect = not_connected+not_connected_new
    random.shuffle(points_to_connect)
    wires2, connected, not_connected2 = get_wires(mainGrid, points_to_connect)
    ## SCORE
    len_list2 = sum([len(i.route) for i in wires2 + old_wires[swaps:]])
    len2 = len(not_connected2)

    if len_list > len_list2 and len1 == len2:
        wires = wires2 + old_wires[swaps:]
        not_connected = not_connected2
    else:
        for w in wires2:
            mainGrid.remove_wire(w)
        for w in old_wires[swaps:]:
            mainGrid.add_wire(w)

    return mainGrid, wires, not_connected

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

def length_score(data_file, wires, percentile, not_connected,
                 cal_time, net_number, points_to_connect):
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
    data = {'netlist':net_number}
    data['total_connected'] = percentile
    data['true_len'] = sum(len_list)
    data['longest'] = max(len_list)
    data['shortest'] = min(len_list)
    data['mean'] = data['true_len'] / len(len_list)
    data['q25'] = len_list[int(len(len_list)/4)]
    data['q75'] = len_list[-int(len(len_list)/4)]
    data['cal_time'] = cal_time
    data['len_percentile'] = sum(len_list)/sum(minlen_list)
    data['starting order'] = str(points_to_connect)
    data['ending order'] = str(not_connected)
    df = pd.read_excel("options.xlsx", sheet_name=0)
    settings = sys.argv[2]
    var = df.iloc[int(settings)]
    data['options'] = str(list(var))
    data['option_num'] = int(settings)

    print(f'\nThe score was: {percentile}')
    print(f'\nThe len was: {sum(len_list)}')
    output(data_file, data)
    print(f'Data is saved in {data_file}')
    return percentile

def make_imported_points(points, netlist):
    start_index, end_index = zip(*netlist)
    starts = [(points[i][0],points[i][1],0) for i in start_index]
    ends = [(points[i][0],points[i][1],0) for i in end_index]
    return ends, starts

def output(filename, data):
    df = pd.read_excel(filename, sheet_name=0)
    data['time'] = str(time.localtime())
    df_new = pd.DataFrame(data, index = [1])
    df_file = df.append(df_new, ignore_index=True, sort=False)
    df_file.to_excel(filename)
