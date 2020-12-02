class LabirintTurtle:
    def __init__(self):
        self.map = []
        self.map_valid = True
        self.turtle_coord = [None, None]
        self.maze_shape = [0, 0]
        self.exit_coord = None
        self.path_len = 0
        self.way = [[-1, -1, -1]]
        self.is_load = False
        self.is_path = False
        self.is_check = False

    def load_map(self, file):
        if file.endswith('.txt'):
            self.is_load = True

            fd = open(file, 'r')
            lines = fd.readlines() # read all lines of file
            last = lines[-2:] # get 2 last lines
            self.turtle_coord[0] = int(last[0])
            self.turtle_coord[1] = int(last[1])
            mz = lines[:-2] # maze is all except 2 last lines

            for line in mz:
                t = list(line[:-1]) # drop \n symbol in end on line
                self.map.append(t)
            fd.close()

            self.maze_shape[0] = len(self.map)
            self.maze_shape[1] = len(self.map[0])

            return 'Карта ' + str(self.maze_shape) + ' загружена.  Координаты черепахи ' + str(self.turtle_coord)
        else:
            return 'Неверный тип файла карты:' + ' ' + str(file.split('.')[1])

    def show_map(self, turtle=False):
        print('>> SHOW MAP', end='')
        if self.is_load:
            tmp = self.map[:]
            if turtle:
                print(' WITH TURTLE')
                tmp[self.turtle_coord[1]][self.turtle_coord[0]] = 'A' # set A in turtle coord
            else:
                print(' WITHOUT TURTLE')
            for i, line in enumerate(tmp):
                print(*line)
            self.map[self.turtle_coord[1]][self.turtle_coord[0]] = ' '

            if self.map_valid and self.is_check:
                return 'Карта валидная'
            elif self.map_valid and not self.is_check :
                return 'Карта непроверена'
            else:
                return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def check_map(self):
        print('>> CHECK MAP')
        if self.is_load: # and self.map_valid:
            # карта может состоять только из символов * и пробелов. - набор символов должен быть ограничен
            for line in self.map:
                for ch in line:
                    if ch != '*' and ch != ' ': # if current symbol is not * or ' '
                        self.map_valid = False
                        return 'Карта невалидная. Неприменимый символ'

            # в карте обязательно должен быть выход - хотя бы один пробел в крайних стенках
            up = self.map[0] # top line
            bottom = self.map[-1] # bottom line
            left = [i[0] for i in self.map] # left line
            right = [i[-1] for i in self.map] # rigth line

            for i in [up, bottom, left, right]:
                ex_c = 0 # counter for founded ' '
                if ' ' in i: # is space in any of bound lines
                    index_x = i.index(' ')
                    if self.map[0][index_x] == ' ':  # up
                        index_y = 0
                    if self.map[-1][index_x] == ' ':  # bottom
                        index_y = self.maze_shape[0] - 1
                    if left[index_x] == ' ':  # left
                        index_y = left.index(' ')
                    if right[index_x] == ' ':  # right
                        index_y = right.index(' ')

                    self.exit_coord = [index_x, index_y]
                    self.is_check = True
                    ex_c += 1
                    break
            if ex_c == 0:
                return 'Карта невалидная. Отсутствует выход / некорректный выход'

            # нет областей из которых выход черепахи невозможен. (Валидная, если черепаха там не стоит(то есть
            # если может найти выход))
            # -- поиск точек, попав в которые, черепаха не может выбраться. Все соседние точки снизу и сверху *
            for row in range(1, self.maze_shape[0] - 1):
                for col in range(1, self.maze_shape[1] - 1):
                    cur = self.map[row][col]

                    prev_x = self.map[row][col - 1]
                    next_x = self.map[row][col + 1]
                    prev_y = self.map[row - 1][col]
                    next_y = self.map[row + 1][col]
                    if cur != '*' and next_x == prev_x and next_x == '*' and next_y == prev_y and next_y == '*':
                        self.map_valid = False
                        return 'Карта невалидная. Непроходимые места'

            # черепашка не может находится на стенке
            if self.turtle_coord[0] is not None:
                x = self.turtle_coord[0]
                y = self.turtle_coord[1]
                if self.map[x][y] == '*':
                    self.map_valid = False
                    return 'Карта невалидная. Черепаха не может находится в стене'

            # в карте есть координаты черепахи
            if self.turtle_coord[0] is None:
                self.map_valid = False
                return 'Карта невалидная. Координаты черепахи не определены'

            return 'Карта валидная'
        else:
            return 'Карта не загружена'

    def exit_count_step(self):
        print('>> EXIT COUNT STEP')
        if self.is_load:
            if self.map_valid or self.is_check:
                # count for each .
                for line in self.map:
                    for c in line:
                        if '.' in c:
                            self.path_len += 1
                if self.path_len == 0:
                    self.path_len = len(self.way[1:])
                    return 'Поиск пути не был реализован'
                else:
                    return 'Длина пути ' + str(self.path_len)

            if self.map_valid and self.is_check:
                return 'Карта валидная'
            elif self.map_valid and not self.is_check:
                return 'Карта непроверена'
            else:
                return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def exit_show_step(self):
        print('>> EXIT SHOW STEP')
        if self.is_load:
            if self.map_valid and self.is_check:
                start = self.turtle_coord
                self.solve(start[0], start[1])

                for r, line in enumerate(self.map):
                    points = line[:]
                    for c, col in enumerate(points):
                        # заменить все полученные символы с буквами на точки
                        if col == 'R' or col == 'L' or col == 'D' or col == 'U':
                            points[c] = '.'
                    print(*points)

                self.is_path = True
                return 'Карта валидная'
            elif self.map_valid and not self.is_check:
                return 'Карта непроверена'
            else:
                return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def name_action(self):
        print('>> NAME ACTION')
        if self.is_load:
            if self.map_valid and self.is_check:
                start = self.turtle_coord
                self.solve(start[0], start[1]) # вызов рекурсивной функции для поиска пути, начиная с координат черепахи
                print('A -> ', end='')
                for step in self.way[1:][::-1]:
                    print(step[0], '-> ', end='')
                print('EXIT')
                self.is_path = True

                return 'Карта валидная'
            elif self.is_load and not self.is_check:
                return 'Карта не проверена'
            elif self.is_load and not self.map_valid:
                return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def solve(self, x, y):
        self.map[self.exit_coord[1]][self.exit_coord[0]] = ':' # обозначить выход :
        if y > len(self.map) - 1 or x > len(self.map[y]) - 1: # если алгоритм попытался выйти за границы карты
            return False

        if self.map[y][x] == ":":  # выход достигнут
            return True

        if self.map[y][x] != " ": # продолжаем поиски
            return False

        self.map[y][x] = "." #

        # рекурсивный вызов
        # если следующая по координатам точка в виде параметра вернет True , записать в карту
        if self.solve(x + 1, y) == True:  # right
            self.way.append(['Right', x, y])
            self.map[y][x] = 'R'
            return True
        if self.solve(x, y + 1) == True:  # down
            self.way.append(['Down', x, y])
            self.map[y][x] = 'D'
            return True
        if self.solve(x - 1, y) == True:  # left
            self.way.append(['Left', x, y])
            self.map[y][x] = 'L'
            return True
        if self.solve(x, y - 1) == True:  # up
            self.way.append(['Up', x, y])
            self.map[y][x] = 'U'
            return True

        # возврат и затирание следов
        self.map[y][x] = " "
        return False

maze = LabirintTurtle()
#print(maze.load_map('test2.txt'))
print(maze.load_map('hard_test.txt'))
#print(maze.show_map(turtle=False))
#print(maze.show_map(turtle=True))
print(maze.check_map())
print(maze.exit_show_step())
print(maze.exit_count_step())
print(maze.name_action())
print(maze.exit_count_step())