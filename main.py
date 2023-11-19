import keyboard
import random
import os

COLS = 10
ROWS = 10
EMPTY = '.'
PLAYER = 'A'

class Cell:
    """
    Класс Cell представляет отдельную ячейку на игровом поле.
    """
    def __init__(self, Y=None, X=None):
        """
        Инициализация объекта Cell.
        """
        self.image = EMPTY
        self.Y = Y
        self.X = X
        self.content = None

    def draw(self):
        """
        Отображение содержимого ячейки.
        Если ячейка пуста, отображается символ EMPTY, иначе отображается символ содержимого.
        """
        if self.content:
            print(self.content.image, end=' ')
        else:
            print(self.image, end=' ')


class Player:
    """
    Класс Player представляет игрока на поле.
    """
    def __init__(self, Y=None, X=None):
        """
        Инициализация объекта Player.
        """
        self.image = PLAYER
        self.Y = Y
        self.X = X

    def move_player(self, direction, field):
        """
        Перемещение игрока на поле.
        """
        new_Y, new_X = self.Y, self.X

        if direction == 'up' and self.Y > 0:
            new_Y -= 1
        elif direction == 'down' and self.Y < field.rows - 1:
            new_Y += 1
        elif direction == 'left' and self.X > 0:
            new_X -= 1
        elif direction == 'right' and self.X < field.cols - 1:
            new_X += 1

        if field.cells[new_Y][new_X].content is None:
            field.cells[self.Y][self.X].content = None
            self.Y, self.X = new_Y, new_X
            field.cells[self.Y][self.X].content = self


class Field:
    """
    Класс Field представляет игровое поле.
    """
    def __init__(self, cell=Cell, player=Player):
        """
        Инициализация объекта Field.
        """
        self.rows = ROWS
        self.cols = COLS
        self.cells = [[cell(Y=y, X=x) for x in range(COLS)] for y in range(ROWS)]
        self.player = player(Y=random.randint(0, ROWS - 1), X=random.randint(0, COLS - 1))
        self.cells[self.player.Y][self.player.X].content = self.player

    def draw_rows(self):
        """
        Отображение всех строк игрового поля.
        """
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()


def clear_screen():
    """
    Очистка экрана консоли, учитывая операционную систему.
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Game:
    """
    Класс Game представляет игровой процесс.
    """

    def __init__(self):
        """
        Инициализация объекта Game.
        """
        self.field = Field()

    def run(self):
        """
        Запуск игрового процесса.
        """
        self.field.draw_rows()

        while True:
            key = keyboard.read_event(suppress=True)
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'esc':
                    print("Game over")
                    return
                if key.name == 'up':
                    self.field.player.move_player('up', self.field)
                    clear_screen()
                    self.field.draw_rows()
                elif key.name == 'down':
                    self.field.player.move_player('down', self.field)
                    clear_screen()
                    self.field.draw_rows()
                elif key.name == 'left':
                    self.field.player.move_player('left', self.field)
                    clear_screen()
                    self.field.draw_rows()
                elif key.name == 'right':
                    self.field.player.move_player('right', self.field)
                    clear_screen()
                    self.field.draw_rows()

Ant_Eater = Game()
Ant_Eater.run()