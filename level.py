from game_objects import Brick, HorizontalBrick, VerticalBrick


class Level:
    def __init__(self, bricks, space):
        self.bricks = bricks
        self.space = space
        self.number = 0
        self.number_of_bolls = 5
        self.count_of_bolls = self.count_of_bolls(self.count_of_bolls)

    def count_of_bolls(self, count):
        return count

    def build_level_0(self):
        x = 840
        y = 105
        brick = VerticalBrick((x, y), self.space)
        brick.isBase = True
        self.bricks.append(brick)

        self.number_of_bolls = 5

    def build_level_1(self):
        x = 840
        y = 75
        brick = HorizontalBrick((x, y), self.space)
        brick.isBase = True
        self.bricks.append(brick)

        self.number_of_bolls = 5

    def load_level(self):
        try:
            build_name = "build_level_" + str(self.number)
            getattr(self, build_name)()
        except AttributeError:
            self.number = 0
            build_name = "build_level_" + str(self.number)
            getattr(self, build_name)()

