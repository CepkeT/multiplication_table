# # print('Hello world')
# while True:
#     wot = input('введи что-нибудь: ')
#     if wot.isdigit():
#         num = int(wot)
#         print(f'Таблица умножения для числа {num}:')
#         table = [f'{num} * {count} = {num * count}' for count in range(0, 100)]
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
    table = [f"│ {num:<9} │ {count:<11} │ {num * count:<9} │" for count in range(0, 100)]
    print('\n'.join(table))
    print("└───────────┴─────────────┴───────────┘")


def test():
    num1 = int(input("введи первое число: "))
    num2 = int(input("введи второе число: "))
    num3 = int(input("введи третье число: "))

    print(f"красавчиг сумма {num1} + {num2} + {num3} = {num1 + num2 + num3}")


def alim_refactor():
    inputnumbercounter = int(input("Введите кол-во вводимых цифр: "))
    inputnumbers = []

    for i in range(1, inputnumbercounter + 1):
        number = int(input(f"Number {i}: "))
        inputnumbers.append(number)

    inputnumberssum = sum(inputnumbers)
    numbers_str = ' + '.join([str(num) for num in inputnumbers])

    print(f"Сумма {numbers_str} = {inputnumberssum}")


if __name__ == "__main__":
    # input_num = int(input('Введите число: '))
    # multiplication_table(input_num)
    # test()
    alim_refactor()
