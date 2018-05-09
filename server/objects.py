

class Character:
    def __init__(self):
        self.position = (10, 10)
        self.direction = 0
        self.current_speed = 5
        self.max_speed = 10

    def serialize(self):
        return {'position': [self.position[0], self.position[1]]}