class Point(Object):

    def __init__(self, location, attribute, neighbours, value):
        self.location = location
        self.attribute = attribute
        self.neighbours = neighbours
        self.value = value

    def get_neighbours(self):
        return self.neighbours

    def get_attribute(self):
        return self.atrribute

    def __str__(self):
        return(f"This point is at location {self.location} and is " +
               f"{self.attribute} with {self.neighbours} as neighbours " +
               f"and has value {self.value}")
