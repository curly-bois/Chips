from point import Point
from grid import Grid
from wire import Wire

from extra import *
from settings import *
from data import get_data
from instance import Instance
from heuristics import  *


import random
import time
import pickle

import os
import sys
import copy
import pickle
import numpy

settings = sys.argv[2]
OUTER_LOOPS = int(sys.argv[3])

df = pd.read_excel(filename, sheet_name=0)
var = df.iloc[int(settings)]

## Settings of the Main loop ##
SWAP = True
LOOPS = int(var[9])
SWAPS = int(var[10])
SORT = True
data_file = r"C:\Users\s147057\Documents\GitHub\Chips\chipSolver\data\new.xlsx"
###############################



if __name__ == '__main__':
    # Get input from command line
    try:
        netlist_number = sys.argv[1]
        settings = int(sys.argv[2])
        options = get_options(settings)
    except:
        print('usage: python main.py #netlist_number')
        sys.exit()

    if not int(netlist_number):
        print('usage: python main.py #netlist_number')
        sys.exit()
    else:
        netlist_number = int(netlist_number)

    print(f'Solving the following netlist #{netlist_number}')


    start_time = time.time()

    # Import data
    ends, starts, tpnum, net_number, SIZE, count_dict = get_data(netlist_number)
    all_points = ends + starts


    points_to_connect = sort_points2(starts, ends) #, count_dict)

    GENS = 30
    generation = [Instance(Grid(SIZE, all_points)) for i in range(GENS)]

    saved_wires = [
                    "wires_4_0_sima_139.p",
                    "wires_4_1_sima_358.p",
                    "wires_4_2_sima_21.p",
                    "wires_4_3_sima_246.p",
                    "wires_4_4_sima_303.p",
                    "wires_4_5_sima_252.p",
                    "wires_4_6_sima_62.p",
                    "wires_4_7_sima_78.p",
                    "wires_4_8_sima_24.p",
                    "wires_4_9_sima_292.p",
                    "wires_4_10_sima_39.p",
                    "wires_4_11_sima_203.p",
                    "wires_4_12_sima_51.p",
                    "wires_4_13_sima_320.p",
                    "wires_4_14_sima_16.p",
                    "wires_4_15_sima_29.p",
                    "wires_4_16_sima_260.p",
                    "wires_4_17_sima_141.p",
                    "wires_4_18_sima_306.p",
                    "wires_4_19_sima_92.p",
                    "wires_4_20_sima_130.p",
                    "wires_4_21_sima_33.p",
                    "wires_4_22_sima_467.p",
                    "wires_4_23_sima_76.p",
                    "wires_4_24_sima_41.p",
                    "wires_4_25_sima_610.p",
                    "wires_4_26_sima_98.p",
                    "wires_4_27_sima_189.p",
                    "wires_4_28_sima_346.p",
                    "wires_4_29_sima_166.p",
    ]

    for i, gen in enumerate(generation):
        # gen = load_gen(gen, name = saved_wires[i], excel_data =  [])
        random.shuffle(points_to_connect)
        Wires, connected, not_connected = get_wires(gen.main,
                                                    points_to_connect)
        # A star algo
        gen.start((Wires, not_connected))
        gen.main.value_grid = second_value(SIZE)

    loops = 30
    MAX = int(tpnum)

    data = []
    for iter in range(loops):
        generation.sort(key=sortbothvalue, reverse=True)
        s1 = generation[0].score1()
        s2 = generation[0].score2()
        data.append((s1,s2))
        print(f'{iter}. Current best:' ,s1 ,'len:' ,s2)
        for i, gen in enumerate(generation):
            random.shuffle(gen.wires)
            random.shuffle(gen.not_connected)
            gen.main, new_wires , new_not_con = swap_wires_plant(gen.gwires(),
                                                        gen.gnotc(),
                                                        gen.main,
                                                        gen.swap)

            gen.snotc(new_not_con)
            gen.swires(new_wires)

        generation.sort(key=sortbothvalue, reverse=True)
        generation_1 = [sortbothvalue(i) for i in generation[:GENS]]

        ma = max(generation_1)
        mi = min(generation_1)

        if mi-ma == 0:
            ma += 0.0000001
            print('fu')

        new_gen = []
        for i, gen in enumerate(generation[:GENS]):
            score = cal_fitness(ma, mi, gen)
            # print('score', score, gen.score1(), gen.score2(), swap_s(score, MAX), repo_s(score))
            generation1 = make_new_gen(gen, repo_s(score), swap_s(score, MAX), SIZE, all_points)
            new_gen += generation1

        del generation
        generation = new_gen


    X = generation[0]
    print(Check(X.wires))
    connected = tpnum - len(X.not_connected)

    # Print lenght + minimal lenght
    cal_time = time.time() - start_time
    score = length_score(data_file,
                         X.wires,
                         connected / tpnum,
                         X.not_connected,
                         cal_time,
                         net_number,
                         data)

    # Time!
    print(f'We found this sollution in: {cal_time}')

    # X.main.plot_wire(X.wires)
    # import pickle
    # pickle.dump( data, open( "data.p", "wb" ) )
    # pickle.dump( X.wires, open( "wires.p", "wb" ) )
