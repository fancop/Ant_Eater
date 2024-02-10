import keyboard
import os
import random
from time import sleep

# ANSI Escape-коды для цветов
COLOR_GREEN = '\033[92m'
COLOR_WHITE = '\033[97m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_RED = '\033[91m'
COLOR_RESET = '\033[0m'

COLS = 10
ROWS = 10
EMPTY = f'{COLOR_GREEN}.{COLOR_RESET}'
PLAYER = f'{COLOR_YELLOW}P{COLOR_RESET}'
ANT = f'{COLOR_RED}a{COLOR_RESET}'
ANTHILL = f'{COLOR_BLUE}A{COLOR_RESET}'
ANTHILL_MAX = 3
ANTHILL_MIN = 1
ANTS_PER_ANTHILL_MAX = 10
ANTS_PER_ANTHILL_MIN = 1


class GameObject:
    '''
    Базовый класс для всех игровых объектов.
    '''

    def __init__(self, y, x, image):
        '''
        Инициализация объекта с указанными координатами и изображением.
        '''
        self.y = y
        self.x = x
        self.image = image

    def move(self, direction, field):
        '''
        Перемещает объект в указанном направлении на игровом поле.
        '''
        new_y, new_x = self.y, self.x

        if direction == 'up' and self.y > 0 and not isinstance(field.cells[self.y - 1][self.x].content, Anthill):
            new_y -= 1
        elif direction == 'down' and self.y < field.rows - 1 and not isinstance(
            field.cells[self.y + 1][self.x].content, Anthill
        ):
            new_y += 1
        elif direction == 'left' and self.x > 0 and not isinstance(field.cells[self.y][self.x - 1].content, Anthill):
            new_x -= 1
        elif direction == 'right' and self.x < field.cols - 1 and not isinstance(
            field.cells[self.y][self.x + 1].content, Anthill
        ):
            new_x += 1

        field.cells[self.y][self.x].content = None
        self.y, self.x = new_y, new_x
        field.cells[self.y][self.x].content = self

    def place_object(self, field):
        '''
        Размещает объект на игровом поле.
        '''
        if field.cells[self.y][self.x].content is None:
            field.cells[self.y][self.x].content = self
        else:
            empty_cells = [
                (i, j)
                for i in range(field.rows)
                for j in range(field.cols)
                if field.cells[i][j].content is None
            ]
            if empty_cells:
                new_y, new_x = random.choice(empty_cells)
                field.cells[new_y][new_x].content = self
                self.y, self.x = new_y, new_x
            else:
                print(f'Нету клеток для размещения {self.image}!')

    def draw(self, field):
        '''
        Рисует объект на игровом поле.
        '''
        field.cells[self.y][self.x].content = self


class Cell:
    '''
    Класс, представляющий клетку игрового поля.
    '''

    def __init__(self, Y=None, X=None):
        '''
        Инициализация клетки с пустым изображением и координатами.
        '''
        self.image = EMPTY
        self.Y = Y
        self.X = X
        self.content = None

    def draw(self):
        '''
        Выводит изображение содержимого клетки.
        '''
        if self.content:
            print(self.content.image, end=' ')
        else:
            print(self.image, end=' ')


class Player(GameObject):
    '''
    Класс игрока на игровом поле.
    '''

    def __init__(self, y=None, x=None):
        '''
        Инициализация игрока с указанными координатами.
        '''
        super().__init__(y, x, PLAYER)

    def move(self, direction, field):
        '''
        Перемещает игрока в указанном направлении на игровом поле.
        '''
        super().move(direction, field)


class Ant(GameObject):
    '''
    Класс представляющий муравья на игровом поле.
    '''

    def __init__(self, y, x):
        '''
        Инициализация муравья с указанными координатами.
        '''
        super().__init__(y, x, ANT)


class Anthill(GameObject):
    '''
    Класс представляющий муравейник на игровом поле.
    '''

    def __init__(self, x, y, quantity):
        '''
        Инициализация муравейника
        с указанными координатами и количеством муравьев.
        '''
        super().__init__(y, x, ANTHILL)
        self.quantity = quantity
        self.spawn_counter = 0
        self.ants_counter = random.randint(
            ANTS_PER_ANTHILL_MIN,
            ANTS_PER_ANTHILL_MAX
        )

    def place(self, field):
        '''
        Размещает муравейник на игровом поле.
        '''
        super().place_object(field)

    def draw(self, field):
        '''
        Рисует муравейник на игровом поле.
        '''
        super().draw(field)


class Field:
    '''
    Класс, представляющий игровое поле.
    '''

    def __init__(self, cell=Cell, player=Player, anthill=Anthill):
        '''
        Инициализация игрового поля с указанными параметрами.
        '''
        self.game_over = False
        self.rows = ROWS
        self.cols = COLS
        self.eaten_ants = 0
        self.escaped_ants = 0
        self.total_ants = 0
        self.anthills = []
        self.ants = []
        self.cells = [
            [cell(Y=y, X=x) for x in range(COLS)] 
            for y in range(ROWS)
        ]
        self.player = player(
            y=random.randint(0, ROWS - 1),
            x=random.randint(0, COLS - 1)
        )
        self.player.place_object(self)
        self.player.draw(self)

    def draw_rows(self):
        '''
        Выводит изображение каждой клетки игрового поля.
        '''
        for row in self.cells:
            for cell in row:
                cell.draw()
            print()

    def add_anthill(self, anthill):
        '''
        Добавляет муравейник на игровое поле.
        '''
        self.anthills.append(anthill)
        anthill.place_object(self)

    def get_neighbours(self, y, x):
        '''
        Возвращает координаты соседних клеток для заданных координат.
        '''
        neighbours_coords = []
        for row in (-1, 0, 1):
            for col in (-1, 0, 1):
                if row == 0 and col == 0:
                    continue
                neighbours_coords.append((y + row, x + col))
        return neighbours_coords

    def add_anthills(self):
        '''
        Добавляет случайное количество муравейников на игровое поле.
        '''
        available_cells = [
            (x, y)
            for x in range(self.cols)
            for y in range(self.rows)
            if (x, y) != (self.player.x, self.player.y)
        ]

        quantity = random.randint(ANTHILL_MIN, ANTHILL_MAX)

        for i in range(quantity):
            if not available_cells:
                break
            anthill_x, anthill_y = random.choice(available_cells)
            available_cells.remove((anthill_x, anthill_y))
            anthill = Anthill(
                x=anthill_x,
                y=anthill_y,
                quantity=random.randint(ANTHILL_MIN, ANTHILL_MAX)
            )
            self.add_anthill(anthill)

        anthill.place_object(self)

    def spawn_ants(self):
        '''
        Создает новых муравьев в муравейниках.
        '''
        self.move_ants()
        for anthill in self.anthills:
            if anthill.ants_counter > 0 and anthill.spawn_counter == 0:
                anthill_x, anthill_y = anthill.x, anthill.y
                neighbors = [
                    (anthill_y - 1, anthill_x - 1),
                    (anthill_y - 1, anthill_x),
                    (anthill_y - 1, anthill_x + 1),
                    (anthill_y, anthill_x - 1),
                    (anthill_y, anthill_x + 1),
                    (anthill_y + 1, anthill_x - 1),
                    (anthill_y + 1, anthill_x),
                    (anthill_y + 1, anthill_x + 1),
                ]
                empty_neighbors = [
                    (y, x)
                    for y, x in neighbors
                    if 0 <= y < self.rows and 0 <= x < self.cols
                    and not self.cells[y][x].content
                ]
                if empty_neighbors:
                    ant_y, ant_x = random.choice(empty_neighbors)
                    ant = Ant(y=ant_y, x=ant_x)
                    self.cells[ant_y][ant_x].content = ant
                    anthill.ants_counter -= 1
                    anthill.spawn_counter = 1
                    self.ants.append(ant)

            if anthill.spawn_counter > 0:
                anthill.spawn_counter += 1
                if anthill.spawn_counter > 4:
                    anthill.spawn_counter = 0

    def move_ants(self):
        '''
        Перемещает муравьев по игровому полю.
        '''
        for ant in self.ants:
            neighbours_coords = self.get_neighbours(ant.y, ant.x)
            random.shuffle(neighbours_coords)
            for y, x in neighbours_coords:
                if y < 0 or y > self.rows - 1 or x < 0 or x > self.cols - 1:
                    if ant in self.ants:
                        self.ants.remove(ant)
                        self.cells[ant.y][ant.x].content = None
                        self.escaped_ants += 1
                    break

                new_cell = self.cells[y][x]
                if new_cell.content:
                    if isinstance(new_cell.content, Player):
                        self.eaten_ants += 1
                        self.ants.remove(ant)
                        self.cells[ant.y][ant.x].content = None
                    continue
                self.cells[ant.y][ant.x].content = None
                new_cell.content = ant
                ant.y = y
                ant.x = x
                break

        ants_in_anthill = sum(anthill.ants_counter for anthill in self.anthills)

        ants_on_field = any(
            cell.content and isinstance(cell.content, Ant)
            for row in self.cells for cell in row
        )

        if ants_in_anthill == 0 and not ants_on_field:
            self.game_over = True

    def update_statistics(self):
        '''
        Обновляет статистику по съеденным и сбежавшим муравьям
        Выводит ее на экран.
        '''
        self.total_ants = self.eaten_ants + self.escaped_ants
        print('Статистика:')
        print(f'Все муравьи: {self.total_ants}')
        print(f'Съеденные мураьи: {self.eaten_ants}')
        print(f'Сбежавшие муравьи: {self.escaped_ants}')
        input(f'{COLOR_RED}Если вы посмотрели статистику, то нажмите ENTER, чтобы закончить игру{COLOR_RESET}')


def clear_screen():
    '''
    Очищает экран консоли.
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


class Game:
    '''
    Класс, представляющий игру и управляющий ею.
    '''

    def __init__(self):
        '''
        Инициализация игры.
        '''
        self.field = Field()
        self.field.add_anthills()

    def handle_keyboard_event(self, event):
        '''
        Обрабатывает события клавиатуры
        Перемещает игрока в соответствии с нажатой клавишей.
        '''
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'up':
                self.field.player.move('up', self.field)
            elif event.name == 'down':
                self.field.player.move('down', self.field)
            elif event.name == 'left':
                self.field.player.move('left', self.field)
            elif event.name == 'right':
                self.field.player.move('right', self.field)
            elif event.name == 'esc':
                print('Игра окончена!')
                return True
        return False

    def update_game_state(self):
        '''
        Обновляет состояние игры: рисует поле, создает новых муравьев
        Проверяет условия завершения игры.
        '''
        clear_screen()
        self.field.draw_rows()
        self.field.spawn_ants()

        if self.field.game_over:
            print('Все муравьи съедены или сбежали. Игра окончена!')

        sleep(0.17)

    def run(self):
        '''
        Запускает игру и обрабатывает события до завершения игры.
        '''
        self.field.draw_rows()

        while not self.field.game_over:
            event = keyboard.read_event(suppress=True)
            if self.handle_keyboard_event(event):
                break

            self.update_game_state()

        clear_screen()
        self.field.draw_rows()
        self.field.update_statistics()


# Создание экземпляра игры и запуск её выполнения
AntEaterGame = Game()
AntEaterGame.run()