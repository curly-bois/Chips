from point import Point
from grid import Grid
from wire import Wire

from extra import *
from settings import *
from data import get_data
from instance import Instance
from heuristics import  plant_prop, plant_prop_lite, sim_annealing, hill_climber


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

    GENS = 10
    generation = [Instance(Grid(SIZE, all_points)) for i in range(GENS)]

    for gen in generation:
        random.shuffle(points_to_connect)
        Wires, connected, not_connected = get_wires(gen.main,
                                                    points_to_connect)
        # A star algo
        gen.start((Wires, not_connected))
        # Reset value grid
        gen, data = sim_annealing(gen, options)
        gen.main.value_grid = second_value(SIZE)


    loops = 10
    MAX = int(tpnum/2)

    def sortbothvalue(g):
        num = g.score1()
        dec = int((2000 - g.score2())*0.5)
        return float(f'{num}.{dec}')


    def cal_fitness(ma, mi, g_class):
        f = ((ma-sortbothvalue(g_class))/(ma-mi))
        f = 1 - f
        return 0.5*(numpy.tanh((4*f)-2)+1)

    def repo_s(score):
        return int(numpy.ceil(5*score*random.random()))

    def swap_s(score, MAX):
        d = ((1-score)*random.random()*MAX)
        return int(numpy.ceil(d))

    data = []
    for iter in range(loops):
        generation.sort(key=sortbothvalue, reverse=True)
        s1 = generation[0].score1()
        s2 = generation[0].score2()
        data.append((s1,s2))
        print(f'{iter}. Current best:' ,s1 ,'len:' ,s2)
        for i, gen in enumerate(generation):
            random.shuffle(gen.wires)
            gen.main, new_wires , new_not_con = swap_wires_plant(gen.gwires(),
                                                        gen.gnotc(),
                                                        gen.main,
                                                        gen.swap)

            # Shuffle wires
            new_wires = shuffle(new_wires)
            new_not_con = shuffle(new_not_con)
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

    X.main.plot_wire(X.wires)
    import pickle
    pickle.dump( data, open( "data.p", "wb" ) )
    pickle.dump( X.wires, open( "wires.p", "wb" ) )
