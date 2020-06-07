from car import Car
from board import Board
from helper import load_json
import sys

CHOOSE_CAR_MSG = 'Please choose a car to move and a direction to move it,' \
                 ' in this format: Car color,direction.\n' \
                 'Make sure that the car is on the board and that the direction' \
                 ' is valid.\n'
TRY_AGAIN_MSG = 'Invalid input.\nPlease try again.' \
                ' \nMake sure that the car is' \
                ' on the board and that the direction is valid.\n'
LEGAL_MOVE_MSG = 'The car is able to move '
VALID_MOVEKEYS = 'r', 'l', 'u', 'd'
RIGHT, LEFT, UP, DOWN = VALID_MOVEKEYS
FREE_CELL = 'E'
WIN_MSG = 'Congratulations, you have won the game!!! What an honor.'
VALID_CARS = ['Y', 'B', 'O', 'G', 'W', 'R']
VERTICAL = 0
HORIZONTAL = 1
TARGET_CELL = (3,7)
COMMA = ','
WELCOME_MSG = 'Welcome To The Game Rush Hour! :)'
CURRENT_STATUS_MSG = 'Action succeed! This is the current state of the board:'


class Game:
    """
    this class contains functions which runs the game together
    """

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.board = board

    def __single_turn(self):
        """
        this function asks for input from the user, then checks if it's valid,
        and if it it valid it moves a car according to the input.
        """

        user_input = input(CHOOSE_CAR_MSG)
        cars_on_board = []
        for car in self.board.cars:
            cars_on_board.append(car.get_name())
        while len(user_input) != 3 or user_input[0] not in cars_on_board or\
                (user_input[0], user_input[2], LEGAL_MOVE_MSG+user_input[2])\
                not in self.board.possible_moves() or user_input[1] != COMMA:
            user_input = input(TRY_AGAIN_MSG)
        self.board.move_car(user_input[0], user_input[2])
        print(CURRENT_STATUS_MSG)
        print(self.board)


    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        while self.board.cell_content(TARGET_CELL) is None:
            self.__single_turn()
        print(WIN_MSG)


if __name__ == "__main__":
    game_board = Board()
    filename = sys.argv[1]
    car_dict = load_json(filename)
    for car_name in car_dict:
        car = Car(car_name, car_dict[car_name][0], car_dict[car_name][1],
                  car_dict[car_name][2])
        if car.get_name() in VALID_CARS:  # here i'm checking if the info from
            if car.length > 0:            #  the json file is valid
                if (car.location[0], car.location[1]) in \
                        game_board.cell_list() and TARGET_CELL not in\
                        car.car_coordinates():
                    if car.orientation == HORIZONTAL or \
                            car.orientation == VERTICAL:
                        game_board.add_car(car)
    game = Game(game_board)
    print(WELCOME_MSG)
    print(game_board)
    game.play()





