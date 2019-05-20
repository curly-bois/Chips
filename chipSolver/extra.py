from point import Point
from wire import Wire

import random
import numpy as np
import pandas as pd
import sys
import time
import math

option_file = r"data\options.xlsx"

def Check(wires):
    all = []
    pointss = []
    for i in wires:
        all += i.route
        pointss.append(i.start)
        pointss.append(i.end)
    all_wire = []
    for a in all:
        if not a in pointss:
            all_wire.append(a)

    return (len(all_wire) == len(set(all_wire)))

def shuffle(items):
    r = [random.randint(0,1) for i in range(len(items))]
    items1 = [items[n]  for n, i in enumerate(r) if i == 1]
    items2 = [items[n]  for n, i in enumerate(r) if i == 0]
    return items1+items2

def update_temperature(T, delta_t):
    # return T - 0.019
    return T * delta_t

def sortit(i):
    return i.score1()

def shortestit(i):
    return i.score2()

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
            # mainGrid.update_layer()
            # mainGrid.wire_NN_edit() ## Commented out
            connected += 1

    return wires, connected, not_connected

def swap_wires(wires, not_connected, mainGrid, swaps):

    len_list = len(not_connected)
    popped_wires = []
    old_wires = [i for i in wires]

    for wire in old_wires[:swaps]:
        coords = mainGrid.remove_wire(wire)
        popped_wires.append(wires.pop(wires.index(wire)))
        not_connected.append(coords)

    wires2, connected, not_connected = get_wires(mainGrid, not_connected)
    len_list2 = len(not_connected)

    if len_list > len_list2:
        wires3 = wires2 + wires
        return mainGrid, wires3, not_connected
    else:
        for w in wires2:
            not_connected.append(mainGrid.remove_wire(w))
        # [(w.start, w.end) for w in wires]
        # [(w.start, w.end) for w in wires2]
        for w in popped_wires:
            not_connected.pop(not_connected.index(mainGrid.add_wire(w)))

        wires3 = popped_wires + wires
        return mainGrid, wires3, not_connected

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    else:
        return math.exp((old_cost - new_cost) / temperature)

def swap_wiresA(wires, not_connected, mainGrid, swaps, t):

    len_list = len(not_connected)
    popped_wires = []
    old_wires = [i for i in wires]

    for wire in old_wires[:swaps]:
        coords = mainGrid.remove_wire(wire)
        popped_wires.append(wires.pop(wires.index(wire)))
        not_connected.append(coords)

    wires2, connected, not_connected = get_wires(mainGrid, not_connected)
    len_list2 = len(not_connected)

    prop = acceptance_probability(len_list, len_list2, t)

    if prop > random.random():
        wires3 = wires2 + wires
        return mainGrid, wires3, not_connected
    else:
        for w in wires2:
            not_connected.append(mainGrid.remove_wire(w))
        # [(w.start, w.end) for w in wires]
        # [(w.start, w.end) for w in wires2]
        for w in popped_wires:
            not_connected.pop(not_connected.index(mainGrid.add_wire(w)))

        wires3 = popped_wires + wires
        return mainGrid, wires3, not_connected

def swap_wiresA_P(wires, not_connected, mainGrid, swaps, t):

    len1 = len(not_connected)
    len_list = sum([len(i.route) for i in wires])
    popped_wires = []
    old_wires = [i for i in wires]

    for wire in old_wires[:swaps]:
        coords = mainGrid.remove_wire(wire)
        popped_wires.append(wires.pop(wires.index(wire)))
        not_connected.append(coords)

    wires2, connected, not_connected2 = get_wires(mainGrid, not_connected)
    len2 = len(not_connected2)

    prop = acceptance_probability(len1, len2, t)
    len_list2 = sum([len(i.route) for i in wires2 + wires])
    prop2 = acceptance_probability(len_list, len_list2, t)

    if ((prop > random.random() or prop2 > random.random()) and prop > random.random()):
        # print('this', len(wires2), len(wires), len(popped_wires))
        # print('this2', len(not_connected), len(not_connected2))
        wires3 = wires2 + wires
        return mainGrid, wires3, not_connected2
    else:
        # print('that', len(wires2), len(wires), len(popped_wires))
        # print('that2', len(not_connected), len(not_connected2))
        for w in wires2:
            not_connected2.append(mainGrid.remove_wire(w))

        for w in popped_wires:
            not_connected2.pop(not_connected2.index(mainGrid.add_wire(w)))

        wires3 = popped_wires + wires
        return mainGrid, wires3, not_connected2

def swap_wires_for_score(wires, not_connected, mainGrid, swaps):

    len_list = sum([len(i.route) for i in wires])
    len1 = len(not_connected)
    popped_wires = []
    old_wires = [i for i in wires]

    for wire in old_wires[:swaps]:
        coords = mainGrid.remove_wire(wire)
        popped_wires.append(wires.pop(wires.index(wire)))
        not_connected.append(coords)

    wires2, connected, not_connected = get_wires(mainGrid, not_connected)
    len_list2 = sum([len(i.route) for i in wires2 + wires])
    len2 = len(not_connected)


    if len_list > len_list2 and len1 >= len2:
        wires3 = wires2 + wires
        return mainGrid, wires3, not_connected
    else:
        for w in wires2:
            not_connected.append(mainGrid.remove_wire(w))
        # [(w.start, w.end) for w in wires]
        # [(w.start, w.end) for w in wires2]
        for w in popped_wires:
            not_connected.pop(not_connected.index(mainGrid.add_wire(w)))

        wires3 = popped_wires + wires
        return mainGrid, wires3, not_connected

def swap_wires_for_scoreA(wires, not_connected, mainGrid, swaps, t):

    len_list = sum([len(i.route) for i in wires])
    len1 = len(not_connected)
    popped_wires = []
    old_wires = [i for i in wires]

    for wire in old_wires[:swaps]:
        coords = mainGrid.remove_wire(wire)
        popped_wires.append(wires.pop(wires.index(wire)))
        not_connected.append(coords)

    wires2, connected, not_connected = get_wires(mainGrid, not_connected)
    len_list2 = sum([len(i.route) for i in wires2 + wires])
    len2 = len(not_connected)

    prop = acceptance_probability(len_list, len_list2, t)

    if (prop > random.random() or len1 > len2) and len1 >= len2:
        wires3 = wires2 + wires
        return mainGrid, wires3, not_connected
    else:
        for w in wires2:
            not_connected.append(mainGrid.remove_wire(w))
        # [(w.start, w.end) for w in wires]
        # [(w.start, w.end) for w in wires2]
        for w in popped_wires:
            not_connected.pop(not_connected.index(mainGrid.add_wire(w)))

        wires3 = popped_wires + wires
        return mainGrid, wires3, not_connected


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
    df = pd.read_excel(option_file, sheet_name=0)
    settings = sys.argv[2]
    var = df.iloc[int(settings)]
    data['options'] = str(list(var))
    data['option_num'] = int(settings)

    print(f'\nThe score was: {percentile}')
    print(f'The len was: {sum(len_list)}')
    output(data_file, data)
    print(f'Data is saved in {data_file}\n')
    return percentile

def make_imported_points(points, netlist):
    start_index, end_index = zip(*netlist)
    starts = [(points[i][0],points[i][1],0) for i in start_index]
    ends = [(points[i][0],points[i][1],0) for i in end_index]

    count_dict = {}
    for i in ends+starts:
        if i in count_dict:
            count_dict[i] +=1
        else:
            count_dict[i] = 1

    return ends, starts, count_dict

def output(filename, data):
    df = pd.read_excel(filename, sheet_name=0)
    data['time'] = str(time.localtime())
    df_new = pd.DataFrame(data, index = [1])
    df_file = df.append(df_new, ignore_index=True, sort=False)
    df_file.to_excel(filename)
