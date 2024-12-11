import random
import logging

# Настройка логирования
logging.basicConfig(filename='./log/games_guess-the-number.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def start_game():
    print("Добро пожаловать в игру 'Угадай число'!")
    print("Я загадал число от 1 до 100.")
    number_to_guess = random.randint(1, 100)
    attempts = 0
    found = False

    while not found:
        try:
            user_guess = int(input("Введите ваше предположение: "))
            attempts += 1
            
            logging.info(f'Пользователь ввел: {user_guess}')

            if user_guess < number_to_guess:
                print("Слишком малое число. Попробуйте еще раз.")
            elif user_guess > number_to_guess:
                print("Слишком большое число. Попробуйте еще раз.")
            else:
                found = True
                print(f"Поздравляем! Вы угадали число {number_to_guess} за {attempts} попыток.")
                logging.info(f'Пользователь угадал число {number_to_guess} за {attempts} попыток.')
        except ValueError:
            print("Пожалуйста, введите корректное число.")
            logging.error("Пользователь ввел недопустимое значение.")

if __name__ == "__main__":
    start_game()
