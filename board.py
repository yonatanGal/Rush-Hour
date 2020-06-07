
BOARD_HEIGHT = 7
BOARD_WIDTH = 7
TARGET_CELL = (3, 7)
VALID_MOVEKEYS = 'r', 'l', 'u', 'd'
RIGHT, LEFT, UP, DOWN = VALID_MOVEKEYS
VERTICAL = 0
HORIZONTAL = 1
FREE_CELL = '_'
LEGAL_MOVE_MSG = 'The car is able to move '
LEFTY_BOUND = 0
RIGHTY_BOUND = 6
UPPER_BOUND = 0
DOWNER_BOUND = 6
EXIT = 'E'


class Board:
    """
    this class creates objects of board type.
    in out game, the board is always 7*7, and the exit point of the board is
    at (3,7).
    """

    def __init__(self):
        """
        A constructor for a board object
        """
        self.board = [['_', '_', '_', '_', '_', '_', '_', '*'],
                      ['_', '_', '_', '_', '_', '_', '_', '*'],
                      ['_', '_', '_', '_', '_', '_', '_', '*'],
                      ['_', '_', '_', '_', '_', '_', '_', 'E'],
                      ['_', '_', '_', '_', '_', '_', '_', '*'],
                      ['_', '_', '_', '_', '_', '_', '_', '*'],
                      ['_', '_', '_', '_', '_', '_', '_', '*']]

        self.cars = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        board_str = ''
        for row in range(BOARD_HEIGHT):
            row_str = ''
            for col in range(BOARD_WIDTH+1):
                row_str += self.board[row][col] + " "
            board_str += row_str + "\n"
        return board_str

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        cells = []
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                cells.append((i, j))
        cells.append(TARGET_CELL)
        return cells

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        possible_moves_lst = []
        for car in self.cars:
            row, col = car.location
            if car.orientation == HORIZONTAL:
                right_row, right_col = car.movement_requirements(RIGHT)[0][0],\
                                     car.movement_requirements(RIGHT)[0][1]
                if right_col <= RIGHTY_BOUND:
                    self.__update_right_direction(car, possible_moves_lst)
                if (right_row, right_col) == TARGET_CELL:
                    possible_moves_lst.append((car.get_name(), RIGHT,
                                               LEGAL_MOVE_MSG + RIGHT))
                if col >= LEFTY_BOUND:
                    self.__update_left_direction(car, col,
                                                 possible_moves_lst, row)
            elif car.orientation == VERTICAL:
                down_row, down_col = car.movement_requirements(DOWN)[0][0],\
                                     car.movement_requirements(DOWN)[0][1]
                if down_row <= DOWNER_BOUND:
                    self.__update_down_direction(car, possible_moves_lst)
                if row > UPPER_BOUND:
                    self.__update_up_direction(car, col, possible_moves_lst,row)
        return possible_moves_lst

    def __update_up_direction(self, car, col, possible_moves_lst, row):
        """ this function checks the up direction and update the
        possible_moves_lst accordingly"""
        if self.board[row][col + 1] == FREE_CELL:
            possible_moves_lst.append((car.get_name(), UP,
                                       LEGAL_MOVE_MSG + UP))

    def __update_down_direction(self, car, possible_moves_lst):
        """ this function checks the down direction and update the
                possible_moves_lst accordingly"""
        cell_to_check = car.movement_requirements(DOWN)
        row, col = cell_to_check[0][0], cell_to_check[0][1]
        if self.board[row][col] == FREE_CELL:
            possible_moves_lst.append((car.get_name(), DOWN,
                                       LEGAL_MOVE_MSG + DOWN))

    def __update_left_direction(self, car, col, possible_moves_lst, row):
        """ this function checks the left direction and update the
                possible_moves_lst accordingly"""
        if self.board[row][col - 1] == FREE_CELL:
            possible_moves_lst.append((car.get_name(), LEFT,
                                       LEGAL_MOVE_MSG + LEFT))

    def __update_right_direction(self, car, possible_moves_lst):
        """ this function checks the right direction and update the
                possible_moves_lst accordingly"""
        cell_to_check = car.movement_requirements(RIGHT)
        row, col = cell_to_check[0][0], cell_to_check[0][1]
        if self.board[row][col] == FREE_CELL or \
                self.board[row][col] == EXIT:
            possible_moves_lst.append((car.get_name(), RIGHT,
                                       LEGAL_MOVE_MSG + RIGHT))

    def target_location(self):
        """
        This function returns the coordinates of the location which is
         to be filled for victory.
        :return: (row,col) of goal location
        """
        return TARGET_CELL

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        i, j = coordinate
        if self.board[i][j] != '_' and self.board[i][j] != EXIT:
            return self.board[i][j]
        else:
            return None

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        for car_on_board in self.cars:
            if self.cars[car_on_board][0] == car.get_name():
                return False
        for coordinate in car.car_coordinates():
            if coordinate not in self.cell_list():
                return False
            if self.cell_content(coordinate) is not None:
                return False
        for coordinate in car.car_coordinates():
            row, col = coordinate
            self.board[row][col] = car.get_name()
        self.cars[car] = [car.get_name(), car.length, car.location,
                          car.orientation]
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        for car in self.cars:
            if car.get_name() == name:
                if movekey == LEFT:
                    if self.__check_and_move_left(car) is True:
                        return True

                elif movekey == RIGHT:
                    if self.__check_and_move_right(car) is True:
                        return True

                elif movekey == UP:
                    if self.__check_and_move_up(car) is True:
                        return True

                elif movekey == DOWN:
                    if self.__check_and_move_down(car) is True:
                        return True
        return False

    def __check_and_move_down(self, car):
        """ this function checks the down direction and update the car
         location accordingly, returns True if the car moves and None if not"""
        i, j = car.movement_requirements(DOWN)[0][0],\
               car.movement_requirements(DOWN)[0][1]
        if car.location[0] != DOWNER_BOUND and self.cell_content((i, j))\
                is None:
            row, col = car.location
            self.board[row][col] = FREE_CELL
            self.board[row + car.length][col] = car.get_name()
            car.move(DOWN)
            return True

    def __check_and_move_up(self, car):
        """ this function checks the up direction and update the car
        location accordingly, returns True if the car moves and None if not"""
        i, j = car.movement_requirements(UP)[0][0],\
               car.movement_requirements(UP)[0][1]
        if car.location[0] != UPPER_BOUND and self.cell_content((i, j)) is None:
            row, col = car.location
            self.board[row - 1][col] = car.get_name()
            self.board[row + car.length - 1][col] = FREE_CELL
            car.move(UP)
            return True

    def __check_and_move_right(self, car):
        """ this function checks the right direction and update the car
        location accordingly, returns True if the car moves and None if not"""
        i, j = car.movement_requirements(RIGHT)[0][0],\
               car.movement_requirements(RIGHT)[0][1]
        if car.location[1]+car.length-1 != RIGHTY_BOUND and \
                self.cell_content((i, j)) is None:
            row, col = car.location
            self.board[row][col] = FREE_CELL
            self.board[row][col + car.length] = car.get_name()
            car.move(RIGHT)
            return True
        elif self.cell_content((i, j)) == EXIT:
            row, col = car.location
            self.board[row][col] = FREE_CELL
            self.board[row][col + car.length] = car.get_name()
            car.move(RIGHT)
            return True
        elif (3, 6) in car.car_coordinates():
            row, col = car.location
            self.board[row][col] = FREE_CELL
            self.board[row][col + car.length] = car.get_name()
            car.move(RIGHT)
            return True

    def __check_and_move_left(self, car):
        """ this function checks the left direction and update the car
        location accordingly, returns True if the car moves and None if not"""
        i, j = car.movement_requirements(LEFT)[0][0],\
               car.movement_requirements(LEFT)[0][1]
        if car.location[1] != LEFTY_BOUND and self.cell_content((i, j)) is None:
            row, col = car.location
            self.board[row][col - 1] = car.get_name()
            self.board[row][col + car.length - 1] = FREE_CELL
            car.move(LEFT)
            return True