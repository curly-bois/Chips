"""
============
3D animation
============

A simple example of an animated plot... In 3D!
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


def plot_anam(rawdata, size, multi = True):

    if multi == False:
        data = []
        line = [[],[],[]]
        max_len = 0
        ends = []
        for l in [i.route for i in rawdata]:
            linex,liney, linez = zip(*l)
            line[0] += linex
            line[1] += liney
            line[2] += linez
            max_len += len(linex)
            ends.append(len(line[0])-1)
        data= np.array([line])

    else:
        data = []
        max_len = 0
        for l in [i.route for i in rawdata]:
            line = [[],[],[]]
            linex,liney, linez = zip(*l)
            line[0] += linex
            line[1] += liney
            line[2] += linez

            if len(linex) > max_len:
                max_len = len(linex)

            data.append(np.array(line))

    def init():
        #init lines
        for line in lines:
            line.set_data([], [])
        return lines

    def update_lines(num, dataLines, lines):
        for line, data in zip(lines, dataLines):
            # NOTE: there is no .set_data() for 3 dim data...
            line.set_data(data[0:2, :num])
            line.set_3d_properties(data[2, :num])
            # line.set_color('green')
        return lines

    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)

    # Creating fifty line objects.
    # NOTE: Can't pass empty arrays into 3d version of plot()
    lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

    # Setting the axes properties
    ax.set_xlim3d([0.0, float(size[0])])
    ax.set_xlabel('X')

    ax.set_ylim3d([0.0, float(size[1])])
    ax.set_ylabel('Y')

    ax.set_zlim3d([0.0, float(size[2])])
    ax.set_zlabel('Z')

    ax.set_title('3D Test')

    # Creating the Animation object
    line_ani = animation.FuncAnimation(fig, update_lines, init_func=init, frames = max_len, fargs=(data, lines),
                                           interval=500, blit=False)

    plt.show()
