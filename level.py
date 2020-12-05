from game_objects import Brick, HorizontalBrick, VerticalBrick


class Level:
    def __init__(self, bricks, space):
        self.bricks = bricks
        self.space = space
        self.number = 0
        self.number_of_balls = 5
        self.count_of_balls = self.count_of_balls(self.number_of_balls)

    def count_of_balls(self, count):
        return count

    def build_level_0(self):
        """level 0"""
        # 1 block level
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
        # 2 block level
        x = 870
        y += 60
        for _ in range(2):
            self.bricks.append(HorizontalBrick((x, y), self.space))
            x += 89
        # 3 block level
        x = 885
        y += 60
        for _ in range(2):
            self.bricks.append(VerticalBrick((x, y), self.space))
            x += 60
        # 4 block level
        x = 915
        y += 60
        self.bricks.append(HorizontalBrick((x, y), self.space))

        self.number_of_balls = 5

    def build_level_1(self):
        """level 1"""
        # 1 block level
        x = 840
        y = 75
        for _ in range(3):
            brick = Brick((x, y), self.space)
            brick.isBase = True
            self.bricks.append(brick)
            x += 60
        # 2 block level
        x = 840
        y += 29
        for _ in range(3):
            x = 840
            for _ in range(3):
                self.bricks.append(Brick((x, y), self.space))
                x += 60
            y += 29

        self.number_of_balls = 5

    def load_level(self):
        try:
            build_name = "build_level_" + str(self.number)
            getattr(self, build_name)()
        except AttributeError:
            self.number = 0
            build_name = "build_level_" + str(self.number)
            getattr(self, build_name)()

