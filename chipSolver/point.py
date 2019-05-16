class Point(object):
    '''
    A point in the grid
    '''

    def __init__(self, location):
        self.location = location
        self.attribute = 'free'
        self.neighbours = []
        self.value = None
        self.g = 0

    def set_neighbour(self, neighbour):
        self.neighbours.append(neighbour)

    def get_neighbours(self):
        return self.neighbours

    def set_attribute(self, attribute):
        self.attribute = attribute

    def get_attribute(self):
        return self.attribute

    def set_value(self, value):
        self.value = value

    def setG(self, g):
        self.g = g

    def __str__(self):
        return(f"This point is at location {self.location} and is " +
               f"{self.attribute} with {self.neighbours} as neighbours " +
               f"and has value {self.value}")
