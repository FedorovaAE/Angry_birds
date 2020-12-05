from game_objects import Brick, HorizontalBrick, VerticalBrick


class Level:
    def __init__(self, bricks, space):
        self.bricks = bricks
        self.space = space
        self.number = 0
        self.number_of_balls = 5
        self.count_of_balls = self.count_of_balls(self.count_of_balls)

    def count_of_balls(self, count):
        return count

    def build_level_0(self):
        x = 840
        y = 105
        for _ in range(2):
            brick = VerticalBrick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        x -= 30
        for _ in range(2):
            brick = VerticalBrick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        x = 870
        y += 60
        for _ in range(2):
            self.bricks.append(HorizontalBrick((x, y), self.space))
            x += 89

        self.number_of_balls = 5

    def build_level_1(self):
        x = 840
        y = 75
        brick = HorizontalBrick((x, y), self.space)
        brick.isBase = True
        self.bricks.append(brick)

        self.number_of_balls = 5

    def load_level(self):
        try:
            build_name = "build_level_" + str(self.number)
            getattr(self, build_name)()
        except AttributeError:
            self.number = 0
            build_name = "build_level_" + str(self.number)
            getattr(self, build_name)()

