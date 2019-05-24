import extra
import sys

def get_data(net_number = 4):
    if not net_number in [1,2,3,4,5,6]:
        print('Net list is not prepared yet, please add to function.')
        sys.exit()

    points = [(1,1),(6,1),(10,1),(15,1),(3,2),(12,2),(14,2),(1,3),(6,3),(12,3),
              (15,3),(2,4),(8,4),(1,5),(4,5),(10,5),(11,5),(16,5),(2,6),(7,6),
              (10,6),(12,6),(15,6),(6,7),(13,7),(16,7),(6,8),(7,8),(9,8),(11,8),
              (15,8),(1,9),(6,9),(9,10),(12,11),(2,12),(4,12),(7,12),(10,12),
              (15,12),(9,13),(13,13),(4,14),(6,14),(1,15),(6,15),(8,15),(11,15),
              (13,15),(16,15)]

    points1 =[(1,1), (6,1), (10,1), (15,1), (3, 2), (12,2), (14,2), (12,3),
              (8,4), (1,5), (4,5), (11,5), (16,5), (13,7), (16,7), (2,8), (6,8),
              (9,8), (11,8), (15,8), (1,9), (2,10), (9,10), (1,11), (12,11)]

    # lengte 30
    netlist_1 = [(23, 4), (5, 7), (1, 0), (15, 21), (3, 5), (7, 13), (3, 23),
                (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18), (19, 2),
                (22, 11), (10, 4), (11, 24), (3, 15), (2, 20), (3, 4), (20, 19),
                (16, 9), (19, 5), (3, 0), (15, 5), (6, 14), (7, 9), (9, 13),
                (22, 16), (10, 7)]

    # lengte 40
    netlist_2 = [(12, 20), (23, 20), (6, 9), (15, 10), (12, 13), (8, 18),
                (1, 22), (10, 20), (4, 3), (10, 5), (17, 11), (1, 21), (22, 8),
                (22, 10), (19, 8), (13, 19), (10, 4), (9, 23), (22, 18),
                (16, 21), (4, 0), (18, 21), (5, 17), (8, 23), (18, 13), (13, 11),
                (11, 7), (14, 7), (14, 6), (14, 1), (24, 12), (11, 15), (2, 5),
                (11, 12), (0, 15), (14, 5), (15, 4), (19, 9), (3, 0), (15, 13)]

    # lengte 50
    netlist_3 = [(0, 13), (0, 14), (0, 22), (8, 7), (2, 6), (3, 19), (3, 9),
                 (4, 8), (4, 9), (5, 14), (6, 4), (4, 1), (7, 23), (10, 0),
                 (10, 1), (8, 1), (7, 5), (12, 14), (13, 2), (8, 10), (11, 0),
                 (11, 17), (11, 3), (8, 9), (12, 24), (13, 4), (13, 19), (15, 21),
                 (10, 3), (18, 10), (24, 23), (16, 7), (17, 15), (17, 21),
                 (17, 9), (18, 20), (18, 2), (12, 9), (1, 13), (19, 21), (20, 6),
                 (1, 15), (2, 16), (20, 16), (22, 11), (22, 18), (2, 3), (5, 12),
                 (24, 15), (24, 16)]



    netlist_4 = [(42, 3), (3, 48), (14, 6), (36, 2), (14, 4), (10, 32), (47, 22),
                 (41, 1), (21, 6), (39, 18), (22, 49), (35, 14), (5, 31), (48, 24),
                 (12, 14), (8, 42), (28, 43), (20, 40), (26, 24), (46, 35), (0, 12),
                 (46, 12), (35, 26), (21, 7), (43, 15), (0, 21), (35, 19), (31, 11),
                 (43, 30), (12, 1), (4, 30), (49, 13), (4, 29), (8, 28), (32, 29),
                 (34, 45), (14, 39), (17, 25), (28, 27), (31, 25), (37, 16), (2, 3),
                 (3, 31), (4, 23), (5, 44), (33, 30), (36, 4), (29, 9), (46, 0),
                 (39, 15)]

    netlist_5 = [(34, 21), (48, 47), (38, 16), (0, 16), (28, 40), (24, 8), (36, 37),
                 (26, 8), (8, 27), (39, 48), (44, 34), (22, 30), (43, 44), (47, 5),
                 (19, 30), (31, 41), (0, 10), (12, 32), (3, 33), (45, 18), (0, 21),
                 (23, 43), (44, 42), (18, 11), (24, 23), (41, 13), (26, 1), (16, 1),
                 (20, 29), (31, 4), (7, 28), (28, 45), (0, 12), (44, 29), (34, 5),
                 (2, 17), (9, 5), (30, 9), (36, 29), (18, 27), (32, 11), (40, 10),
                 (4, 40), (35, 6), (17, 3), (10, 19), (25, 24), (20, 47), (12, 25),
                 (4, 15), (19, 33), (33, 36), (1, 3), (13, 49), (25, 49), (15, 42),
                 (33, 4), (27, 22), (4, 8), (12, 24)]

    netlist_6 = [(16, 10), (25, 17), (1, 11), (32, 2), (1, 20), (12, 36), (34, 19),
                 (11, 10), (11, 45), (21, 42), (36, 20), (15, 22), (3, 21), (48, 2),
                 (32, 25), (38, 49), (24, 29), (14, 16), (0, 3), (30, 7), (3, 10),
                 (16, 8), (46, 0), (26, 41), (34, 2), (1, 13), (25, 6), (49, 28),
                 (27, 47), (3, 14), (40, 47), (14, 43), (14, 46), (27, 38), (14, 34),
                 (26, 39), (47, 44), (46, 29), (12, 9), (49, 12), (38, 7), (30, 32),
                 (30, 40), (13, 45), (5, 41), (29, 37), (45, 38), (44, 34), (44, 28),
                 (22, 44), (43, 31), (48, 34), (6, 33), (33, 7), (1, 37), (5, 17),
                 (37, 2), (39, 38), (27, 36), (18, 42), (17, 35), (12, 5), (37, 40),
                 (5, 39), (37, 43), (8, 4), (39, 3), (33, 31), (21, 33), (0, 39)]


    net_dict = {
                1:netlist_1,
                2:netlist_2,
                3:netlist_3,
                4:netlist_4,
                5:netlist_5,
                6:netlist_6
    }

    if net_number in [4,5,6]:
        SIZE = (18,17,7)
        points = points
    elif net_number in [1,2,3]:
        SIZE = (18,13,7)
        points =points1

    netlist = net_dict[net_number]

    total_poits_number = len(netlist)
    starts,ends, count_dict = extra.make_imported_points(points, netlist)

    return ends, starts, total_poits_number, net_number, SIZE, count_dict
