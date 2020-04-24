from lab3 import *


class Player:
    """
    method: move self.current,
            self.min_step,
            self.max_step,
            self.goal
    """

    def __init__(self, name: str) -> None:
        """
        Initalize a player whose playing a take-turn game
        """
        self.name = name

    def move(self, current: int, min_step, max_step, goal) -> None:
        raise NotImplementedError


class UserPlayer(Player):

    def move(self, current: int, min_step: int, max_step: int, goal: int):
        while True:
            amount_str = input(f'Enter a number for move: ')
            if amount_str.isdigit():
                amount = int(amount_str)
                if amount < min_step or int(amount_str) > max_step or int(amount_str) + current >= goal:
                    print('Please enter the right amount')
                else:
                    break
            else:
                print(f'{amount_str} is not a number, please enter a number only. Lets try again')
        return amount






