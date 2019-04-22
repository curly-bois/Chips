

class Wire(object):
    '''
    A wire in the grid, nice to save some essentials 
    '''
    def __init__(self, start, end, route):
        self.start = start
        self.end = end
        self.route = route
        self.length = len(route)
