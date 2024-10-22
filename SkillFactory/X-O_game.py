def play_me() -> None:
    """
     Главная функция, запускающая программу.

     Другие функции программы запускаются внутри главной функции, что позволяет
     многократно использовать программу.
     :return: None
     """
    batle_field = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']] #Переменная batle_field ссылается на список списков, которые служат для отображения игрового поля и фиксации вводимой информации.
    print('\nДобро пожаловать в игру крестики-нолики.\n')
    print('Игроки по очереди ставят на свободные клетки поля 3×3 знаки\n'
          '(один всегда крестики, другой всегда нолики). Первый, выстроивший\n'
          'в ряд 3 своих фигуры по вертикали, горизонтали или большой диагонали, выигрывает.\n'
          'Если игроки заполнили все 9 ячеек и оказалось, что ни в одной вертикали,\n'
          'горизонтали или большой диагонали нет трёх одинаковых знаков, партия считается\n'
          'закончившейся вничью. Первый ход делает игрок, ставящий крестики.')
    print()

    def show_batle_field() -> None:
        """
        Функция отображает игровое поле в консоли.
        :return: None
        """
        print(' ', '0', '1', '2')
        for i in range(3):
           for j in range(3):
                if j == 0:
                    print(i, end=' ')
                print(f'{batle_field[i][j]}', end=' ')
           print()
        print()

    def player_move() -> None:
        """
        Функция служит для ввода пользователями информации с полседующей её проверкой на соответствие:
        :return: None

        Функция:
        1. считает очерёдность хода;
        2. запрашивает от пользователя информацию (координаты) хода в виде целых чисел int;
        3. проверяет содержит ли ответ пользователя цыфры;
        4. если цифры есть переводит ответ пользователя из строкового значения в числовое;
        5. проверяет полученные целые числа на попадание в диапазон игрового поля;
        6. проверяет клетки игрового поля на занятость;
        7. если не все проверки пройдены, программа повторно предлагает ввести координаты;
        8. если проверка пройдена, функция записывает символ (Х или O) в игровое поле;
        9. после записи результата проверки в игровое поле функция проверяет есть ли
        победитель или на поле ничейная позиция;
        10. если есть победитель и ничья функция завершает программу.
        """
        move_counter = 0 #переменная - счётчик ходов является ключевым
                         #элементом для прохождения проверок введённой пользователем информации.
        while move_counter < 9: # В данном фрагменте кода цыкл необходим для определения очередности хода.
            if move_counter % 2 == 0: # Если ход чётный, ходит первый игрок, используя символ 'X'
                mark = 'X'
                print('Первый игрок сделайте свой ход:')

            elif move_counter % 2 != 0:  # Если ход нечётный, ходит второй игрок, используя символ 'O'
                mark = 'O'
                print('Второй игрок сделайте свой ход:')


            line_coordinate = input('введите координату строки в диапзоне от 0 до 2: ')
            column_coordinate = input('введите координату столбца в диапзоне от 0 до 2: ')

            if not line_coordinate.isdigit() or not column_coordinate.isdigit(): #В данном фрагменте проверяется информация
                print('Ошибка ввода.\nПопробуйте ещё раз.') #на наличие целых чисел.
                show_batle_field()
                continue

            line_coordinate = int(line_coordinate)
            column_coordinate = int(column_coordinate)
            if not line_coordinate in (0, 1, 2) or not column_coordinate in (0, 1, 2): #Проверка на вхождение
                print('Ошибка ввода.\nПопробуйте ещё раз.')                             #введённых данных в диапазон игрового поля.
                show_batle_field()
                continue
            if batle_field[line_coordinate][column_coordinate] != '-': # проверка на занятость поля.
               print('Это поле уже занято.\nПопробуйте ещё раз.')
               show_batle_field()
               continue

            batle_field[line_coordinate][column_coordinate] = mark # Фиксация символа в клетке игрового поля.
            show_batle_field()

            if (mark == batle_field[0][0] == batle_field[0][1] == batle_field[0][2]   #Проверка на наличие победителя:
                    or mark == batle_field[1][0] == batle_field[1][1] == batle_field[1][2] #проверка
                    or mark == batle_field[2][0] == batle_field[2][1] == batle_field[2][2] # по горизонталям;
                    or mark == batle_field[0][0] == batle_field[1][0] == batle_field[2][0] # проверка
                    or mark == batle_field[0][1] == batle_field[1][1] == batle_field[2][1] # по
                    or mark == batle_field[0][2] == batle_field[1][2] == batle_field[2][2] # вертикалям;
                    or mark == batle_field[0][0] == batle_field[1][1] == batle_field[2][2] # проверка по
                    or mark == batle_field[0][2] == batle_field[1][1] == batle_field[2][0]): # по диагоналям.
                print('Блестящая победа!\nПоздравляем!!!\n')
                break

            if move_counter == 8: # Фрагмент кода, проверяющий ничейное положение на игровом поле.
                print('Ничья.\nИгра закончена.\n')
                break

            move_counter += 1 #После завершения хода счётчик ходов прибаляет единицу

    show_batle_field()
    player_move()

while True: # Цыкл и фрагмент кода, позволяющие запустить программу для повторной игры
    offer = input('Хотите сыграть в крестики-нолики? (да/нет): ') # или завершить её по желанию пользователя.
    offer = offer.lower()
    if offer == 'да':
        play_me()
    if offer == 'нет':
        print('Хорошего вам дня.')
        break