HORIZONTAL = 1
VERTICAL = 0
INVALID_MOVE_MSG = 'invalid move, please try again'
MOVEMENTS = 'r', 'l', 'u', 'd'
RIGHT, LEFT, UP, DOWN = MOVEMENTS
LEFT_BORDER = 0
UP_BORDER = 0
RIGHT_BORDER = 6
DOWN_BORDER = 6


class Car:
    """
    This class is responsible for anything about the cars in the game.
    """
    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        if length > 0:
            self.length = length
        else:
            self.length = 0
        self.location = location
        self.orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        coordinates_lst = []
        j, k = self.location
        if self.orientation == VERTICAL:
            for m in range(self.length):
                coordinates_lst.append((j+m, k))
        elif self.orientation == HORIZONTAL:
            for n in range(self.length):
                coordinates_lst.append((j, k+n))
        return coordinates_lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
         permitted by this car.
        """
        possible_moves_dict = {}
        if self.orientation == VERTICAL:
            possible_moves_dict['u'] = 'the car is able to move up'
            possible_moves_dict['d'] = 'the car is able to move down'
        elif self.orientation == HORIZONTAL:
            possible_moves_dict['l'] = 'the car is able to move left'
            possible_moves_dict['r'] = 'the car is able to move right'
        return possible_moves_dict

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order
         for this move to be legal.
        """
        row, col = self.location
        if movekey == LEFT:
            return [(row, col-1)]
        elif movekey == RIGHT:
            return [(row, col+self.length)]
        elif movekey == DOWN:
            return [(row+self.length, col)]
        elif movekey == UP:
            return [(row-1, col)]

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        i, j = self.location
        if movekey == LEFT:
            if self.orientation == HORIZONTAL:
                self.location = i, j-1
                return True
        elif movekey == RIGHT:
            if self.orientation == HORIZONTAL:
                self.location = i, j+1
                return True
        elif movekey == UP:
            if self.orientation == VERTICAL:
                self.location = i-1, j
                return True
        elif movekey == DOWN:
            if self.orientation == VERTICAL:
                self.location = i+1, j
                return True
        return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name