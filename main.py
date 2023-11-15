class Cell:
    def __init__(self, image='С', Y=None, X=None):
        self.image = image
        self.Y = Y
        self.X = X

class Field:
    def __init__(self, rows=10, cols=25, cell=Cell):
        self.rows = rows
        self.cols = cols
        self.cells = [[cell(Y=y, X=x) for x in range(cols)] for y in range(rows)]

    def drawrows(self):
        for row in self.cells:
            print(*[cell.image for cell in row])

MyClass = Field()
MyClass.drawrows()