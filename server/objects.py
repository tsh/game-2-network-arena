

class Character:
    def __init__(self):
        self.position = [10, 10]
        self.direction = 0
        self.current_speed = 5
        self.max_speed = 10

    def move(self, direction=None):
        self.position = (self.position[0] + 1, self.position[1])
        print('self.pos', self.position)

    def serialize(self):
        print('char_pos', self.position)
        return {'position': [self.position[0], self.position[1]]}