class Set(object):

    def __init__(self, startpoint, endpoint, is_connected=False):
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.route = []
        self.is_connected = is_connected

    def get_startpoint(self):
        return self.startpoint

    def get_endpoint(self):
        return self.endpoint

    def set_route(self, route):
        self.route = route

    def get_route(self):
        return self.route

    def is_it_connected(self):
        return self.is_connected

    def __str__(self):
        if self.route:
            this_route = []
            for path in self.route:
                this_route.append(path.get_location())
            return (f"This set goes from {self.startpoint.get_location()} to {self.endpoint.get_location()} and it is {self.is_connected} that is is connected, it takes the following route: {this_route}\n")
        return (f"This set goes from {self.startpoint.get_location()} to {self.endpoint.get_location()} and it is {self.is_connected} that is is connected\n")
