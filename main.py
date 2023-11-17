import random

class Cell:
    """Класс, представляющий ячейку поля."""
    def __init__(self, image='.', Y=None, X=None):
        self.image = image
        self.Y = Y
        self.X = X
        self.content = None 

class Player:
    """Класс, представляющий игрока."""

    def __init__(self, image='A', Y=None, X=None):
        """Инициализация игрока."""
        self.image = image
        self.Y = Y
        self.X = X

class Field:

    def __init__(self, rows=10, cols=10, cell=Cell, player=Player):
        """Инициализация игрового поля."""
        self.rows = rows
        self.cols = cols
        self.cells = [[cell(Y=y, X=x) for x in range(cols)] for y in range(rows)]
        self.player = player(Y=random.randint(0, rows-1), X=random.randint(0, cols-1))
        self.cells[self.player.Y][self.player.X].content = self.player

    def draw_rows(self):
        """Отображение содержимого полей в виде строк."""
        for row in self.cells:
            for cell in row:
                if cell.content is not None:
                    print(cell.content.image, end=' ')
                else:
                    print(cell.image, end=' ')
            print()

AntEater = Field()
AntEater.draw_rows()
