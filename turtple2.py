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
            lines = fd.readlines()
            last = lines[-2:]
            self.turtle_coord[0] = int(last[0])
            self.turtle_coord[1] = int(last[1])
            mz = lines[:-2]

            for line in mz:
                t = list(line[:-1])
                self.map.append(t)
            fd.close()

            self.maze_shape[0] = len(self.map)
            self.maze_shape[1] = len(self.map[0])

            return 'Карта ' + str(self.maze_shape) + ' загружена.  Координаты черепахи ' + str(self.turtle_coord)
        else:
            return 'Неверный тип файла карты:' + ' ' + str(file.split('.')[1])

    def show_map(self, turtle=False):
        if self.is_load and self.map_valid or self.is_check:
            tmp = self.map[:]
            if turtle:
                tmp[self.turtle_coord[1]][self.turtle_coord[0]] = 'A'
            for i, line in enumerate(tmp):
                print(*line)
            self.map[self.turtle_coord[1]][self.turtle_coord[0]] = ' '
            print('-' * 25)
            return ''
        elif self.is_load and not self.map_valid:
            return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def check_map(self):
        if self.is_load and self.map_valid:
            # карта может состоять только из символов * и пробелов. - набор символов должен быть ограничен
            if self.map_valid:
                for line in self.map:
                    if '\t' in line:  # or '\n' in line:
                        self.map_valid = False
                        break

            # в карте обязательно должен быть выход - хотя бы один пробел в крайних стенках
            if self.map_valid:
                f = False
                up = self.map[0]
                bottom = self.map[-1]
                left = [i[0] for i in self.map]
                right = [i[-1] for i in self.map]

                for i in [up, bottom, left, right]:
                    if ' ' in i:
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
                        f = True
                        self.is_check = True
                        break

                self.map_valid = f
            # нет областей из которых выход черепахи невозможен. (Валидная, если черепаха там не стоит(то есть
            # если может найти выход))
            if self.map_valid:
                for row in range(1, self.maze_shape[0] - 1):
                    for col in range(1, self.maze_shape[1] - 1):
                        cur = self.map[row][col]

                        prev_x = self.map[row][col - 1]
                        next_x = self.map[row][col + 1]
                        prev_y = self.map[row - 1][col]
                        next_y = self.map[row + 1][col]
                        if cur != '*' and next_x == prev_x and next_x == '*' and next_y == prev_y and next_y == '*':
                            self.map_valid = False
                            break

            # черепашка не может находится на стенке
            if self.map_valid:
                if self.turtle_coord[0] is not None:
                    x = self.turtle_coord[0]
                    y = self.turtle_coord[1]
                    if self.map[x][y] == '*':
                        self.map_valid = False

            # в карте есть координаты черепахи
            if self.map_valid:
                if self.turtle_coord[0] is None:
                    self.map_valid = False

            if self.map_valid:
                return 'Карта валидная'
            else:
                return 'Карта невалидная'
        elif self.is_load and not self.map_valid:
            return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def exit_count_step(self):
        if self.is_load and self.map_valid and self.is_path:
            for line in self.map:
                for c in line:
                    if '.' in c:
                        self.path_len += 1
            if self.path_len == 0:
                self.path_len = len(self.way[1:])

            return 'Длина пути ' + str(self.path_len)
        elif self.is_load and not self.map_valid:
            return 'Карта невалидная'
        elif self.is_load and self.map_valid and not self.is_path:
            return 'Поиск пути еще не реализован'
        else:
            return 'Карта не загружена'

    def exit_show_step(self):
        if self.is_load and self.map_valid and self.is_check:
            start = self.turtle_coord
            self.solve(start[0], start[1])

            for r, line in enumerate(self.map):
                points = line[:]
                for c, col in enumerate(points):
                    if col == 'R' or col == 'L' or col == 'D' or col == 'U':
                        points[c] = '.'
                print(*points)

            self.is_path = True
            return ''
        elif self.is_load and not self.is_check:
            return 'Карта не проверена на валидность'
        elif self.is_load and not self.map_valid :
            return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def name_action(self):
        if self.is_load and self.map_valid and self.is_check:
            start = self.turtle_coord
            self.solve(start[0], start[1])
            print('A -> ', end='')
            for step in self.way[1:][::-1]:
                print(step[0], '-> ', end='')
            print('EXIT')
            self.is_path = True
            return ''
        elif self.is_load and not self.is_check:
            return 'Карта не проверена на валидность'
        elif self.is_load and not self.map_valid :
            return 'Карта невалидная'
        else:
            return 'Карта не загружена'

    def solve(self, x, y):
        self.map[self.exit_coord[1]][self.exit_coord[0]] = ':'
        if y > len(self.map) - 1 or x > len(self.map[y]) - 1:
            return False

        if self.map[y][x] == ":":
            return True

        if self.map[y][x] != " ":
            return False

        self.map[y][x] = "."

        # рекурсивный вызов
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
print(maze.show_map(turtle=False))
print(maze.show_map(turtle=True))
print(maze.check_map())
print(maze.exit_show_step())
print(maze.exit_count_step())
print(maze.name_action())
print(maze.exit_count_step())