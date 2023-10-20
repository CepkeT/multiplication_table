from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler , D
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
            return  # Стопить дальнейшей ход на доске

        elif all(board[row][col] != ' ' for row in range(3) for col in range(3)):
            # Draw
            await query.message.reply_text('Ничья!')
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
                return  # Стопить дальнейший ход на доске

            elif all(board[row][col] != ' ' for row in range(3) for col in range(3)):
                # Draw
                await query.message.reply_text('Draw!')
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
    # Clear the game board
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '

    await update.message.reply_text('Tic Tac Toe')

    # Send a message to each player with the game board and their symbol
    for i, player in enumerate(players):
        symbol = PLAYER_X if i == 0 else PLAYER_O
        keyboard = [
            [
                InlineKeyboardButton(' ', callback_data=f'move_{symbol}_{row}_{col}')
                for col in range(3)
            ]
            for row in range(3)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(chat_id=player.id, text=f'Your move: {symbol}', reply_markup=reply_markup)


async def start_game(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user

    if user.id in [u.id for u in game_queue]:
        if len(game_queue) >= 1:
            await update.message.reply_text('You are already in the game queue!')
        else:
            await update.message.reply_text('You are already in the game queue! Waiting for another player...')
        return

    game_queue.append(user)

    await update.message.reply_text('Ты добавлен в очередь')

    # Process the game queue
    await process_game_queue(update, context)

    # Clear the game board
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '

    await update.message.reply_text('крестики нолики')

    # Отправить сообщение с кнопками выбора хода
    keyboard = [
        [
            InlineKeyboardButton(' ', callback_data='move_X_0_0'),
            InlineKeyboardButton(' ', callback_data='move_X_0_1'),
            InlineKeyboardButton(' ', callback_data='move_X_0_2'),
        ],
        [
            InlineKeyboardButton(' ', callback_data='move_X_1_0'),
            InlineKeyboardButton(' ', callback_data='move_X_1_1'),
            InlineKeyboardButton(' ', callback_data='move_X_1_2'),
        ],
        [
            InlineKeyboardButton(' ', callback_data='move_X_2_0'),
            InlineKeyboardButton(' ', callback_data='move_X_2_1'),
            InlineKeyboardButton(' ', callback_data='move_X_2_2'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Твой ход', reply_markup=reply_markup)


# Функция для обновления кнопок после каждого хода
async def update_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    player, row, col = query.data.split('_')[1:]

    # Обновляем символ игрока на поле
    board[int(row)][int(col)] = player

    # Обновляем кнопки с символами X и O
    keyboard = [
        [
            InlineKeyboardButton('X' if board[row][col] == PLAYER_X else ' ' if board[row][col] == ' ' else 'O',
                                 callback_data=f'move_{player}_{row}_{col}')
            for col in range(3)
        ]
        for row in range(3)
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_reply_markup(reply_markup)


# Создаем экземпляр приложения
app = ApplicationBuilder().token("6581992513:AAFSuk41_gC3avbA70xqcCpJUx1xXChBzMo").build()

# Добавляем обработчики команд
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("play", start_game))

# Добавляем обработчик для выбора хода
app.add_handler(CallbackQueryHandler(make_move, pattern='^move_[XO]_[0-2]_[0-2]$'))

# Запускаем приложение
app.run_polling()
