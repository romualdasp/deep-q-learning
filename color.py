class Color():
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    dark_grey = (30, 30, 30)
    light_grey = (80, 80, 80)
    white = (255, 255, 255)

    def __init__(self, color):
        self.color = color

    def get(self):
        return self.color