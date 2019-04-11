class Point(object):

    def __init__(self, location, attribute, neighbours, value):
        self.location = location
        self.attribute = attribute
        self.neighbours = neighbours
        self.value = value

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def get_neighbours(self):
        return self.neighbours

    def set_attribute(self, attribute):
        self.attribute = attribute

    def get_attribute(self):
        return self.attribute

    def __str__(self):
        return(f"This point is at location {self.location} and is " +
               f"{self.attribute} with {self.neighbours} as neighbours " +
               f"and has value {self.value}")
