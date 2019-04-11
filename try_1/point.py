class Point(Object):

    def __init__(self, location, attribute, neighbours, value):
        self.location = location
        self.attribute = attribute
        self.neighbours = neighbours
        self.value = value

    def get_neighbours(self):
        return self.neighbours
