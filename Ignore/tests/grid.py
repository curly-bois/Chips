import matplotlib.pyplot as plt


def make_grid(netlist, lines, size = 25):
    '''
    Visualize points and lines on the grid
    '''
    # Convert data to useful data
    size += 1
    x,y = zip(*netlist)

    # scatter points
    plt.figure(figsize=(16,16))
    plt.scatter(x, y, linewidths=8, color='red')

    # Plot lines
    if type(lines) == list:
        for l in lines:
            linex,liney = zip(*l)
            plt.plot(linex, liney, linewidth=5, color='blue')
    else:
        linex,liney = zip(*lines)
        plt.plot(linex, liney, linewidth=5, color='blue')

    # Set range and differnce per line (one)
    plt.xticks(range(0,size,1))
    plt.yticks(range(0,size,1))

    # Set view limit
    plt.xlim([-1,size])
    plt.ylim([-1,size])

    # activate grid
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    netlist_1 = [(23, 4), (5, 7), (1, 0), (15, 21), (3, 5), (7, 13), (3, 23),
                 (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18),
                 (19, 2), (22, 11), (10, 4), (11, 24), (3, 15), (2, 20),
                 (3, 4), (20, 19), (16, 9), (19, 5), (3, 0), (15, 5),
                 (6, 14), (7, 9), (9, 13), (22, 16), (10, 7)]
    lines = [[(10, 14), (9, 14), (9, 13), (9, 12), (9, 11), (9, 10), (9, 9),
              (9, 8), (9, 7), (8, 7), (7, 7), (7, 6), (7, 5), (6, 5), (5, 5),
              (5, 4), (5, 3), (5, 2), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
              (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1), (16, 1),
              (17, 1), (18, 1), (19, 1), (20, 1), (21, 1), (22, 1), (23, 1),
              (24, 1), (25, 1), (26, 1), (26, 2), (25, 2), (24, 2), (23, 2),
              (22, 2), (21, 2), (20, 2), (19, 2), (18, 2), (17, 2), (16, 2),
              (15, 2), (14, 2), (13, 2), (12, 2), (11, 2), (10, 2), (9, 2),
              (8, 2), (7, 2), (6, 2), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3),
              (11, 3), (12, 3), (13, 3), (14, 3), (15, 3), (15, 4), (14, 4),
              (13, 4), (12, 4), (11, 4), (10, 4), (9, 4), (8, 4), (7, 4), (6, 4)]]
    make_grid(netlist_1, lines)
