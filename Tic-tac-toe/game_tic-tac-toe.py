import subprocess
import sys
import logging

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

try:
    import colorama
except ImportError:
    install('colorama')
    
from colorama import Fore, Style, init
init(autoreset=True)
tux = r"""
      .--.
     |o_o |
     |:_/ |
    //   \ \
   (|     | )         Game Tic Tac Toe
  /'\_   _/`\   
  \___)=(___/
"""

print(Fore.MAGENTA + tux)

# Настройка логирования
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

debug_handler = logging.FileHandler("game_tic-tac-toe-debug_info.log", mode='w')
debug_handler.setLevel(logging.DEBUG)
debug_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
debug_handler.setFormatter(debug_format)

warning_handler = logging.FileHandler("game_tic-tac-toe-warnings_errors.log", mode='w')
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(debug_format)

logger.addHandler(debug_handler)
logger.addHandler(warning_handler)


class Cell:
    def __init__(self, number):
        self.number = number
        self.symbol = ' '
        self.occupied = False

    def occupy(self, symbol):
        if not self.occupied:
            self.symbol = symbol
            self.occupied = True
            logger.debug(f"Клетка {self.number} занята {symbol}.")
            return True
        logger.warning(f"Клетка {self.number} уже занята.")
        return False


class Board:
    def __init__(self):
        self.cells = [Cell(i) for i in range(1, 10)]

    def display_board(self):
        print(Fore.YELLOW + f"""
        {self.cells[0].symbol} | {self.cells[1].symbol} | {self.cells[2].symbol}
        ---------
        {self.cells[3].symbol} | {self.cells[4].symbol} | {self.cells[5].symbol}
        ---------
        {self.cells[6].symbol} | {self.cells[7].symbol} | {self.cells[8].symbol}
        """)
        logger.debug("Выводим доску.")
    def change_cell(self, number, symbol):
        if 1 <= number <= 9:
            return self.cells[number - 1].occupy(symbol)
        logger.warning(f"Неверный номер ячейки: {cell_number}. Ход не выполнен")
        return False

    def check_game_over(self):
        winning_combinations = [
            [self.cells[0], self.cells[1], self.cells[2]],
            [self.cells[3], self.cells[4], self.cells[5]],
            [self.cells[6], self.cells[7], self.cells[8]],
            [self.cells[0], self.cells[3], self.cells[6]],
            [self.cells[1], self.cells[4], self.cells[7]],
            [self.cells[2], self.cells[5], self.cells[8]],
            [self.cells[0], self.cells[4], self.cells[8]],
            [self.cells[2], self.cells[4], self.cells[6]],
        ]
        
        for combo in winning_combinations:
            if combo[0].symbol == combo[1].symbol == combo[2].symbol and combo[0].symbol != ' ':
                return True
        return False

    def reset_board(self):
        for cell in self.cells:
            cell.symbol = ' '
            cell.occupied = False


class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.victories = 0
    
    def make_move(self):
        while True:
            try:
                move = int(input(f"{self.name}, введите номер клетки (1-9) для хода: "))
                return move
            except ValueError:
                print("Пожалуйста, введите корректное число.")


class Game:
    def __init__(self):
        self.board = Board()
        self.players = []

    def play_turn(self, player):
        self.board.display_board()
        move = player.make_move()
        if self.board.change_cell(move, player.symbol):
            if self.board.check_game_over():
                player.victories += 1
                logger.info(f"{player.name} победил!")
                print(Fore.GREEN + f"{player.name} победил!")
                return True
            return False
        else:
            logger.warning(f"{player.name} попытался сделать неверный ход.")
            print("Эта клетка уже занята или неверный номер. Попробуйте снова.")
            return self.play_turn(player)

    def play_one_game(self):
        self.board.reset_board()
        while True:
            if self.play_turn(self.players[0]):
                break
            if self.play_turn(self.players[1]):
                break
        self.show_score()

    def show_score(self):
        print(f"Текущий счёт: {self.players[0].name}: {self.players[0].victories}, {self.players[1].name}: {self.players[1].victories}")

    def start_games(self):
        while True:
            self.players.clear()
            name1 = input(Fore.CYAN + "Введите имя первого игрока: " + Style.RESET_ALL)
            symbol1 = Fore.RED + 'X'
            self.players.append(Player(name1, symbol1))

            name2 = input(Fore.CYAN + "Введите имя второго игрока: " + Style.RESET_ALL)
            symbol2 = Fore.GREEN + 'O'
            self.players.append(Player(name2, symbol2))

            self.play_one_game()
            continue_playing = input("Хотите сыграть ещё раз? (да/нет): ").strip().lower()
            if continue_playing != 'да':
                break


if __name__ == "__main__":
    game = Game()
    game.start_games()