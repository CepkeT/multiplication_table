from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
import random


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
def display_board(board):
    for row in board:
        print('|'.join([symbol if symbol != ' ' else ' ' for symbol in row]).replace('X', 'X ').replace('O', 'O '))


# Функция для проверки выигрышной комбинации
def check_win(board, player):
    # Проверяем горизонтальные комбинации
    for row in board:
        if row.count(player) == 3:
            return True

    # Проверяем вертикальные комбинации
    for col in range(3):
        if [board[row][col] for row in range(3)].count(player) == 3:
            return True

    # Проверяем диагональные комбинации
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True

    return False


# Функция для обработки хода игрока
async def make_move(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    player, row, col = query.data.split('_')[1:]

    # Проверяем, что клетка пустая
    if board[int(row)][int(col)] == ' ':
        # Ставим символ игрока на поле
        board[int(row)][int(col)] = player

        # Проверяем состояние игры
        if check_win(board, player):
            # Игрок победил
            await query.message.reply_text(f'Игрок {player} победил!')
        elif all(board[row][col] != ' ' for row in range(3) for col in range(3)):
            # Ничья
            await query.message.reply_text('Ничья!')
        else:
            # Ход бота
            bot_player = PLAYER_O if player == PLAYER_X else PLAYER_X
            bot_row, bot_col = make_bot_move()
            board[bot_row][bot_col] = bot_player

            # Проверяем состояние игры после хода бота
            if check_win(board, bot_player):
                # Бот победил
                await query.message.reply_text(f'Бот {bot_player} победил!')
            elif all(board[row][col] != ' ' for row in range(3) for col in range(3)):
                # Ничья
                await query.message.reply_text('Ничья!')
            else:
                # Ход следующего игрока
                await query.message.reply_text(f'Ход игрока {player}')

    else:
        # Клетка уже занята
        await query.message.reply_text('Эта клетка уже занята!')

    # Обновляем отображение игрового поля
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


# Функция для начала игры
async def start_game(update: Update, context: CallbackContext) -> None:
    # Очищаем игровое поле
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '

    # Отправляем сообщение с инструкцией
    await update.message.reply_text('Игра крестики-нолики началась! Ход игрока X')

    # Отправляем сообщение с кнопками для выбора хода
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

    # Update button labels with X and O symbols
    for row in range(3):
        for col in range(3):
            if board[row][col] == PLAYER_X:
                keyboard[row][col].text = 'X'
            elif board[row][col] == PLAYER_O:
                keyboard[row][col].text = 'O'

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Ваш ход:', reply_markup=reply_markup)


# Создаем экземпляр приложения
app = ApplicationBuilder().token("6581992513:AAFSuk41_gC3avbA70xqcCpJUx1xXChBzMo").build()

# Добавляем обработчики команд
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("play", start_game))

# Добавляем обработчик для выбора хода
app.add_handler(CallbackQueryHandler(make_move, pattern='^move_[XO]_[0-2]_[0-2]$'))

# Запускаем приложение
app.run_polling()
