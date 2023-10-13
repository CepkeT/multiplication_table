# # print('Hello world')
# while True:
#     wot = input('введи что-нибудь: ')
#     if wot.isdigit():
#         num = int(wot)
#         print(f'Таблица умножения для числа {num}:')
#         for i in range(0, 100):
#             result = num * i
#             print(f'{num} * {i} = {result}')
#     elif wot == '0':
#         print('я все')
#         break
#
# def MainOne():
#     num = int(input('введи число: '))
#     print(f'Таблица умножения для числа {num}:')
#     table = [f'{num} * {count} = {num * count}' for count in range(0, 100)]
#     print('\n'.join(table))
#
# MainOne()


def multiplication_table(num):
    print(f'Таблица умножения для числа {num}:')
    print("┌───────────┬─────────────┬───────────┐")
    print("│ Число     │ Множитель   │ Результат │")
    print("├───────────┼─────────────┼───────────┤")
    table = [f"│ {num:<9} │ {i:<11} │ {num * i:<9} │" for i in range(0, 100)]
    print('\n'.join(table))
    print("└───────────┴─────────────┴───────────┘")

if __name__ == "__main__":
    input_num = int(input('Введите число: '))
    multiplication_table(input_num)
