

class Map:
    def __init__(self):
        self.map = [[1,1,1,1],
                    [1,0,1,1],
                    [1,1,1,1]]

    def serialize(self):
        return self.map