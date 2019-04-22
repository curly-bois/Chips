

class Wire(object):
    '''
    A wire in the grid, nice to save some essentials
    '''
    def __init__(self, start, end, route, tries):
        self.start = start
        self.end = end
        self.route = route
        self.tries = tries
        self.length = len(route)
        self.min_len = (abs(start[0] - end[0]) +
                        abs(start[1] - end[1]))
