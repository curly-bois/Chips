class Grid(object):

    def __init__(self, x,y, points):
        self.grid = [[True for i in range(y)] for i in range(x)]
        self.mark_list_taken(points)
        self.wires = []

    def is_free(self, point):
        try:
            if not self.grid[point[0]][point[1]]:
                return False
        except:
            return False
        return True

    def mark_taken(self, point):
        self.grid[point[0]][point[1]] = False

    def mark_list_taken(self, points):
        for p in points:
            self.grid[p[0]][p[1]] = False

    def add_wire(self, wire):
        self.wires.append(wire)

    def get_wires(self):
        return [i.wire_pos() for i in self.wires]

class Wire(object):

    def __init__(self, start_point):
        self.points = [start_point]

    def add_point(self, point):
        self.points.append(point)

    def get_len(self):
        return len(self.points)

    def get_start(self):
        return self.points[0]

    def wire_pos(self):
        return self.points[0:]
