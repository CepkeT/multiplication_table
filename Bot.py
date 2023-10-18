from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
import random
import time

game_queue = []  # Список игроков, которые играют в данный момент


def play_fireworks():
    # Display fireworks animation
    print("Fireworks animation...")
    time.sleep(2)  # Sleep for 2 seconds to simulate the animation
    print("Fireworks animation finished!")


# Создаем пустое поле для игры
board = [[' ' for _ in range(3)] for _ in range(3)]

# Определяем символы для игроков
PLAYER_X = 'X'
PLAYER_O = 'O'

# Определяем состояния игры
STATE_IN_PROGRESS = 'in_progress'
STATE_WIN_X = 'win_x'
STATE_WIN_O = 'win_o'
STATE_DRAW = 'draw'


# Функция для отображения игрового поля
def display_board(board_b):
    for row in board_b:
        print('|'.join([symbol if symbol != ' ' else ' ' for symbol in row]).replace('X', 'X ').replace('O', 'O '))


# Функция для проверки выигрышной комбинации
def check_win(board_b, player):
    # Проверяем горизонтальные комбинации
    for row in board_b:
        if row.count(player) == 3:
            return True

    # Проверяем вертикальные комбинации
    for col in range(3):
        if [board_b[row][col] for row in range(3)].count(player) == 3:
            return True

    # Проверяем диагональные комбинации
    if board_b[0][0] == board_b[1][1] == board_b[2][2] == player:
        return True
    if board_b[0][2] == board_b[1][1] == board_b[2][0] == player:
        return True

    return False


async def make_move(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    player, row, col = query.data.split('_')[1:]

    # Check if the user is the current player
    if update.effective_user.id != game_queue[0].id:
        await query.message.reply_text('It is not your turn!')
        return

    # Проверка, что клетка не занята
    if board[int(row)][int(col)] == ' ':
        # символ игрока на доске
        board[int(row)][int(col)] = player

        # проверка состояния игры после хода игрока
        if check_win(board, player):
            # Игрок выиграл
            await query.message.reply_text(f'Игрок {player} победил!')
            play_fireworks()  # анимация(потомXD)
            game_queue.clear()  # Clear the game queue
            return  # Стопить дальнейшей ход на доске

        elif all(board[row][col] != ' ' for row in range(3) for col in range(3)):
            # Draw
            await query.message.reply_text('Ничья!')
            game_queue.clear()  # Clear the game queue
            return  # Стопить дальнейшей ход на доске

        else:
            # Ход бота
            bot_player = PLAYER_O if player == PLAYER_X else PLAYER_X
            bot_row, bot_col = make_bot_move()
            board[bot_row][bot_col] = bot_player

            #  проверка состояния игры после хода бота
            if check_win(board, bot_player):
                # Бот выиграл
                await query.message.reply_text(f'Бот {bot_player} победил!')
                play_fireworks()  # анимация(потомXD)
                game_queue.clear()  # Clear the game queue
                return  # Стопить дальнейший ход на доске

            elif all(board[row][col] != ' ' for row in range(3) for col in range(3)):
                # Draw
                await query.message.reply_text('Draw!')
                game_queue.clear()  # Clear the game queue
                return  # Стопить дальнейший ход на доске

        # Обновление кнопок
        await update_buttons(update, context)

    else:
        # Клетка занята
        await query.message.reply_text('Клетка занята')

    # обновление поля игры
    display_board(board)


# Функция для хода бота
def make_bot_move():
    # Генерируем случайные координаты для хода бота
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    bot_row, bot_col = random.choice(empty_cells)
    return bot_row, bot_col


# Функция для приветствия
async def hello(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Эй, {update.message.from_user.first_name}!, тебе че надо?')


async def process_game_queue(update: Update, context: CallbackContext) -> None:
    # Check if there are at least two users in the game queue
    if len(game_queue) >= 2:
        # Clear the game queue
        players = game_queue[:2]
        del game_queue[:2]

        # Start the game for the first two players in the queue
        await start_game_for_players(players, update, context)


async def start_game_for_players(players, update: Update, context: CallbackContext) -> None:
   The code you provided is a Python script for a Tic Tac Toe game bot using the Telegram API. It allows users to play Tic Tac Toe against a bot. The bot logic is implemented in the `make_move` function, which handles the user's move and the bot's move.

To fix the issue where the bot still thinks you are playing even after the game has ended, you need to clear the `game_queue` list after the game is finished. You can add the following line of code at the end of the `make_move` function:
game_queue.clear()