import datastruct
import load

def main(txt):
    # Make grid
    points, size_grid = load.get_grid(txt)

    # class Wire
    grid = datastruct.Grid(size_grid, size_grid, points)

    # Choose first point
    maxi = [sum(i) for i in points]
    index = maxi.index(min(maxi))

    # First point and end point
    xstart = points[index][0]
    ystart = points[index][1]

    pop_points = points
    pop_points.pop(index)
    distance = [abs(i[0]-xstart)+abs(i[1]-ystart) for i in pop_points]
    closest_point = pop_points[distance.index(min(distance))]

    # Setup loop
    first = True
    a_points = pop_points

    # Loop until empty
    while len(a_points) > 0:

        if first:
            cur = (xstart, ystart)
            line = datastruct.Wire(cur)
            end = closest_point
            first = False
        else:
            a_points.pop(a_points.index(end))
            if not a_points == []:
                distance = [abs(i[0]-end[0])+abs(i[1]-end[1]) for i in a_points]
                closest_point = a_points[distance.index(min(distance))]
                cur = end
                end = closest_point
            else:
                cur = end
                end = (xstart, ystart)
            line = datastruct.Wire(cur)


        while True:
            pos = [(cur[0]+1,cur[1]),
                   (cur[0]-1,cur[1]),
                   (cur[0],cur[1]+1),
                   (cur[0],cur[1]-1)]

            if end in pos:
                line.add_point(end)
                break

            fail = []
            for i,p in enumerate(pos):
                if not grid.is_free(p):
                    fail.append(i)

            good_pos = [pos[i] for i in range(len(pos)) if not i in fail]
            pos = good_pos

            distance = [abs(i[0]-end[0])+abs(i[1]-end[1]) for i in pos]
            c_p = pos[distance.index(min(distance))]
            try:
                c_p = pos[distance.index(min(distance))]
            except:
                print(f"no combinations at line: {line.points()}")
                break

            grid.mark_taken(c_p)
            line.add_point(c_p)
            cur = c_p

        grid.add_wire(line)

    return grid.get_wires()
