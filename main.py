from colorama import init, Fore
from telegram.ext import Updater, MessageHandler, Filters, ExtBot
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import CallbackQuery, ReplyKeyboardRemove
import random
import math
from time import sleep
import sys
import sqlite3
import requests

updater = Updater('5102501109:AAEq0uyJj_Gy4pb3QbyHQMjzU7ayV26Q7iE', use_context=True)


# ВСЕ НОВЫЕ КОМАНДЫ ЗАСОВЫВАТЬ В FALLBACKS!!!
# Через них возвращать DEFINE, из-за чего процесс распознавания команд будет непрерывным и игра не завершится!

dp = updater.dispatcher
con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
cur = con.cursor()
money = cur.execute("""SELECT * FROM money""").fetchall()  # выбираем все данные из таблицы

print(f'Что такое {money}')
cur.close()
init()
running = True
money_game = False  # идёт игра в монетку или в карты
card_game = False
cards_n = 36
cards = ['PIK', 'TRE', 'CHER', 'BUB']
card = 0
vel_card = {'Шесть': 1, 'Семь': 2, 'Восемь': 3, 'Девять': 4, 'Десять': 5, 'Валет': 6, 'Дама': 7, 'Король': 8, 'Туз': 9}
n_player_cards = 6
n_bot_cards = 6
already_started = 0
CARDS = {
    'PIK': {
        9: 'Туз_PIK',
        8: 'Король_PIK',
        7: 'Дама_PIK',
        6: 'Валет_PIK',
        1: 'Шесть_PIK',
        2: 'Семь_PIK',
        3: 'Восемь_PIK',
        4: 'Девять_PIK',
        5: 'Десять_PIK'
    },
    'TRE': {
        99: 'Туз_TRE',
        88: 'Король_TRE',
        77: 'Дама_TRE',
        66: 'Валет_TRE',
        11: 'Шесть_TRE',
        22: 'Семь_TRE',
        33: 'Восемь_TRE',
        44: 'Девять_TRE',
        55: 'Десять_TRE'
    },
    'CHER': {
        999: 'Туз_CHER',
        888: 'Король_CHER',
        777: 'Дама_CHER',
        666: 'Валет_CHER',
        111: 'Шесть_CHER',
        222: 'Семь_CHER',
        333: 'Восемь_CHER',
        444: 'Девять_CHER',
        555: 'Десять_CHER'
    },
    'BUB': {
        9999: 'Туз_BUB',
        8888: 'Король_BUB',
        7777: 'Дама_BUB',
        6666: 'Валет_BUB',
        1111: 'Шесть_BUB',
        2222: 'Семь_BUB',
        3333: 'Восемь_BUB',
        4444: 'Девять_BUB',
        5555: 'Десять_BUB'
    }
}

answering = ''  # отвечающий (ходит: игрок, отвечает: бот)
bot_answer_answer = ''  # ответ бота на ход игрока (для того, чтобы можно было передавать по функциям)

DEFINE, DEFINE_CARD, DEFINE_PLAYER_ANSWER, LOGIN_NIKNAME, LOGIN_PASSWORD, START, REGISTER, COIN = range(8)

player = list()
bot = list()
first_turn = 'player'     # можно поставить на player, чтобы он всегда начинал ходить первым
cozir = ''
koloda = ['Туз_BUB', 'Король_BUB', 'Дама_BUB', 'Валет_BUB', 'Десять_BUB', 'Девять_BUB', 'Восемь_BUB', 'Семь_BUB',
          'Шесть_BUB',
          'Туз_PIK', 'Король_PIK', 'Дама_PIK', 'Валет_PIK', 'Десять_PIK', 'Девять_PIK', 'Восемь_PIK', 'Семь_PIK',
          'Шесть_PIK',
          'Туз_CHER', 'Король_CHER', 'Дама_CHER', 'Валет_CHER', 'Десять_CHER', 'Девять_CHER', 'Восемь_CHER',
          'Семь_CHER', 'Шесть_CHER',
          'Туз_TRE', 'Король_TRE', 'Дама_TRE', 'Валет_TRE', 'Десять_TRE', 'Девять_TRE', 'Восемь_TRE', 'Семь_TRE',
          'Шесть_TRE']

koloda_forever = ['Туз_BUB', 'Король_BUB', 'Дама_BUB', 'Валет_BUB', 'Десять_BUB', 'Девять_BUB', 'Восемь_BUB',
                  'Семь_BUB', 'Шесть_BUB',
                  'Туз_PIK', 'Король_PIK', 'Дама_PIK', 'Валет_PIK', 'Десять_PIK', 'Девять_PIK', 'Восемь_PIK',
                  'Семь_PIK', 'Шесть_PIK',
                  'Туз_CHER', 'Король_CHER', 'Дама_CHER', 'Валет_CHER', 'Десять_CHER', 'Девять_CHER', 'Восемь_CHER',
                  'Семь_CHER', 'Шесть_CHER',
                  'Туз_TRE', 'Король_TRE', 'Дама_TRE', 'Валет_TRE', 'Десять_TRE', 'Девять_TRE', 'Восемь_TRE',
                  'Семь_TRE', 'Шесть_TRE']


def show_cards(update, context):
    global cozir
    s = ''
    s += f'Козырь: {cozir}\n'
    s += f'Ваши карты: \n'
    for i in player:
        s += f'{player.index(i) + 1}: {i}\n'
    update.message.reply_text(s)

    return DEFINE


def giving_cards(n, update, context):
    global cards_n
    global first_turn, koloda, cozir, cozir_flag

    for i in range(n):
        card = random.choice(koloda)
        player.append(card)
        del koloda[koloda.index(card)]

    for i in range(n):
        card = random.choice(koloda)
        bot.append(card)
        del koloda[koloda.index(card)]

    cozir = random.choice(koloda)
    cozir_flag = True
    del koloda[koloda.index(cozir)]

    show_cards(update, context)
    min_bot = ''
    for card in bot:
        if card.split('_')[1] == cozir.split('_')[1]:
            if min_bot == '':
                min_bot = card
            elif koloda_forever.index(card) > koloda_forever.index(min_bot):
                min_bot = card
            else:
                pass
        else:
            pass

    if min_bot != '':
        index_bot = koloda_forever.index(min_bot)
    else:
        index_bot = -1
    min_player = ''
    for card in player:
        if card.split('_')[1] == cozir.split('_')[1]:
            if min_player == '':
                min_player = card
            elif koloda_forever.index(card) > koloda_forever.index(min_player):
                min_player = card
            else:
                pass
        else:
            pass

    if min_player != '':
        index_player = koloda_forever.index(min_player)
    else:
        index_player = -1

    if first_turn != 'player':
        if min_bot != '' and min_player != '':
            if index_player > index_bot:
                first_turn = 'player'
                print('ПЕРВЫЙ ХОДИТ ИГРОК')
            elif index_player < index_bot:
                first_turn = 'bot'
                print('ПЕРВЫЙ ХОДИТ БОТ')
        elif min_bot == '' and min_player != '':
            first_turn = 'player'
            print('ПЕРВЫЙ ХОДИТ ИГРОК')
        elif min_bot != '' and min_player == '':
            first_turn = 'bot'
            print('ПЕРВЫЙ ХОДИТ БОТ')
        else:
            first_turn = 'player'
            print('ПЕРВЫЙ ХОДИТ ИГРОК')
        cards_n = 23
    else:
        print('ПЕРВЫЙ ХОДИТ ИГРОК')


def exit():
    global running
    running = False
    return running


def player_choose_card(update, context):
    global answering
    update.message.reply_text('Выберите карту:')
    show_cards(update, context)
    answering = 'bot'

    return DEFINE_CARD


def player_move(update, context):
    global n_bot_cards, n_player_cards, cozir_flag, card, answering
    answering = 'bot'
    print(f'Карта плэйер мува {card}')
    move = True

    while move:
        answ = player[card - 1]
        n_player_cards -= 1

        if n_player_cards == 0:     # если число карт == 0
            update.message.reply_text('Вы молодец!')
            pobeda('p', update, context)
        del player[player.index(player[card - 1])]

        if n_player_cards < 6:      # добавление карт if number of cards < 6
            if len(koloda) != 0:
                card = random.choice(koloda)
                player.append(card)
                del koloda[koloda.index(card)]
                n_player_cards += 1

            elif cozir_flag:
                player.append(cozir)
                cozir_flag = False
                n_player_cards += 1

        bot_answ(update, context, answ)
        update.message.reply_text('Теперь ходит бот')
        bot_move(update, context)
        move = False


def player_answer(bot_hod, update, context):
    global player, n_player_cards, n_bot_cards, cozir, coz, cozir_flag, card, answering
    Flag = False
    move = True
    answering = 'player'
    print(f'Карта ансвера {card}')

    while move:
        if player[card - 1].split('_')[1] != cozir.split('_')[1]:
            if bot_hod.split('_')[1] == player[card - 1].split('_')[1]:
                if vel_card[player[card - 1].split('_')[0]] > vel_card[bot_hod.split('_')[0]]:
                    player_answ = player[card - 1]
                    Flag = True
                else:
                    update.message.reply_text('Выбранная вами карта не побивает ' + bot_hod)
                    return player_choose_answer(bot_answer_answer, update, context)
            else:
                update.message.reply_text('Выбранная вами карта не побивает ' + bot_hod)
                return player_choose_answer(bot_answer_answer, update, context)

        elif bot_hod.split('_')[1] != cozir.split('_')[1]:
            Flag = True
            player_answ = player[card - 1]

        else:
            if vel_card[player[card - 1].split('_')[0]] > vel_card[bot_hod.split('_')[0]]:
                player_answ = player[card - 1]
                Flag = True
            else:
                update.message.reply_text('Выбранная вами карта не побивает ' + bot_hod)

        if Flag:
            update.message.reply_text('Вы побили ' + bot_hod + ' картой ' + player_answ)
            del player[card - 1]
            n_player_cards -= 1

            if n_player_cards == 0:     # победа игрока
                print('ВЫ ВЫИГРАЛИ')
                pobeda('p', update, context)

            if n_player_cards < 6:      # раздача карт
                if len(koloda) != 0:
                    card = random.choice(koloda)
                    player.append(card)
                    del koloda[koloda.index(card)]
                    n_player_cards += 1
                elif cozir_flag:
                    player.append(cozir)
                    cozir_flag = False
                    n_player_cards += 1

            move = False
            update.message.reply_text('Теперь ваш ход, удачи')
            player_choose_card(update, context)


def player_choose_answer(bot_hod, update, context):
    global answering, bot_answer_answer
    update.message.reply_text('Чем ответим?')
    show_cards(update, context)
    update.message.reply_text('Напишите <взять>, если хотите взять')
    answering = 'player'
    bot_answer_answer = bot_hod

    return DEFINE_CARD


def bot_move(update, context):
    global bot, cards_n, cozir, n_bot_cards, n_player_cards, cozir_flag, answering
    spisok_card = {'Шесть': [], 'Семь': [], 'Восемь': [], 'Девять': [], 'Десять': [], 'Валет': [], 'Дама': [],
                   'Король': [], 'Туз': []}
    answ = []
    answering = 'player'

    for i in bot:
        if len(koloda) > 0:
            if i.split('_')[1] == cozir.split('_')[1]:
                pass
            else:
                spisok_card[i.split('_')[0]].append(i)
        else:
            spisok_card[i.split('_')[0]].append(i)

    for i in spisok_card.keys():
        if answ == []:
            if len(spisok_card[i]) >= 2:
                answ = spisok_card[i]
            elif len(answ) < 2 and bool(spisok_card[i]):
                answ = spisok_card[i]

    print(f'\nБот атакует {answ[0]}')
    del bot[bot.index(answ[0])]
    n_bot_cards -= 1

    if n_bot_cards == 0:    # победа бота
        update.message.reply_text('БОТ ВЫИГРАЛ')
        pobeda('b', update, context)

    if n_bot_cards < 6:
        if len(koloda) != 0:
            card = random.choice(koloda)
            bot.append(card)
            del koloda[koloda.index(card)]
            n_bot_cards += 1

        elif cozir_flag:
            bot.append(cozir)
            cozir_flag = False
            n_bot_cards += 1

    print(f'Ошибка от бота: {answ[0]}, {type(answ[0])}')
    update.message.reply_text('Бот атакует: ' + answ[0])
    player_choose_answer(answ[0], update, context)


def bot_taking_cards(carta, update, context):
    global n_bot_cards
    bot.append(carta)
    n_bot_cards += 1
    return player_choose_card(update, context)


def bot_answ(update, context, movek):
    global bot, vel_card, cozir, n_player_cards, n_bot_cards, cozir_flag, answering
    answering = 'bot'
    answ = ''
    print(f'\nКарты бота: {bot}')

    for i in bot:
        if i.split('_')[1] == movek.split('_')[1]:
            if answ == '':
                if vel_card[movek.split('_')[0]] > vel_card[i.split('_')[0]]:
                    pass
                else:
                    answ = i
            else:
                if vel_card[movek.split('_')[0]] > vel_card[i.split('_')[0]]:
                    pass
                elif vel_card[i.split('_')[0]] > vel_card[answ.split('_')[0]]:
                    answ = i
    if answ != '':
        print(f'Ответ бота: {answ}')
        update.message.reply_text(f'Ответ бота: {answ}')
        del bot[bot.index(answ)]
        n_bot_cards -= 1

        if n_bot_cards == 0:
            update.message.reply_text('Бот победил!')
            pobeda('b', update, context)

        if n_bot_cards < 6:
            if len(koloda) != 0:
                card = random.choice(koloda)
                bot.append(card)
                del koloda[koloda.index(card)]
                n_bot_cards += 1
            elif cozir_flag:
                bot.append(cozir)
                cozir_flag = False
                n_bot_cards += 1
    else:
        if len(koloda) > 5:
            pass
        elif movek.split('_')[1] != cozir.split('_')[1]:
            for i in bot:
                if answ == '':
                    answ = i
                else:
                    if vel_card[i.split('_')[0]] > vel_card[answ.split('_')[0]]:
                        answ = i
                    else:
                        pass
        if answ == '':
            update.message.reply_text('Бот не может отбиться, бот принимает')
            return bot_taking_cards(movek, update, context)   # здесь начинается ошибка
        else:
            update.message.reply_text('Бот бьет ' + movek + ' картой ' + answ)
            del bot[bot.index(answ)]
            n_bot_cards -= 1

            if n_bot_cards == 0:
                update.message.reply_text('Бот победил!')
                pobeda('b', update, context)

            if n_bot_cards < 6:
                if len(koloda) != 0:
                    card = random.choice(koloda)
                    bot.append(card)
                    del koloda[koloda.index(card)]
                    n_bot_cards += 1

                elif cozir_flag:
                    bot.append(cozir)
                    cozir_flag = False
                    n_bot_cards += 1


def game(update, context):
    global first_turn
    giving_cards(6, update, context)
    if first_turn == 'player':
        controls(update, context)
    elif first_turn == 'bot':
        print('Бот ходит')
        bot_move(update, context)


def pobeda(who_wins, update, context):
    global money, card_game
    if who_wins == 'p':
        print('МОЛОДЕЦ')
        sqlite_connection = sqlite3.connect('ananas_bd.sqlite')  # импортируем базу данных
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = cursor.execute("""DELETE from money
        where nik = ?""", (nik)).fetchall()
        sqlite_connection.commit()
        cursor.close()
        con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
        cursor = con.cursor()
        sqlite_insert_query = """INSERT INTO money VALUES ('""" + nik + "', '" + str(int(money) + 50) + "')"
        count = cursor.execute(
            sqlite_insert_query)  # добавляем в таблицу пользователей и их счета пользователя и счет
        con.commit()
        cursor.close()
        money = str(int(money) + 50)
        update.message.reply_text('Ваш баланс: ' + str(money))
        card_game = False
        return ConversationHandler.END

    if who_wins == 'b':
        print('НЕ ПОВЕЗЛО? ПОПРОБУЙ ЕЩЕ РАЗ')
        sqlite_connection = sqlite3.connect('ananas_bd.sqlite')  # импортируем базу данных
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = cursor.execute("""DELETE from money
        where nik = ?""", (nik)).fetchall()
        sqlite_connection.commit()
        cursor.close()
        con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
        cursor = con.cursor()
        sqlite_insert_query = """INSERT INTO money VALUES ('""" + nik + "', '" + str(int(money) - 50) + "')"
        count = cursor.execute(
            sqlite_insert_query)  # добавляем в таблицу пользователей и их счета пользователя и счет
        con.commit()
        cursor.close()
        money = str(int(money) - 50)
        update.message.reply_text('Ваш баланс: ' + str(money))
        card_game = False
        return ConversationHandler.END


def stop(update, context):
    global already_started
    already_started = 0
    update.message.reply_text('Выходим...', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def controls(update, context):
    reply_keyboard = [['Посмотреть карты', 'Сделать ход'],
                      ['Управление', 'Выход']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Что вы хотите сделать?',
                              reply_markup=markup)

    return DEFINE


def go(update, context):
    update.message.reply_text('Доброго времени суток! Пожалуйста войдите в свой аккаунт или зарегистрируйтесь')
    update.message.reply_text('Введите свой никнейм')
    return LOGIN_NIKNAME


def define_card(update, context):
    global card, answering, n_player_cards, player
    card = update.message.text      # получаем сообщение из player_choose_card

    if answering == 'player' and card == 'взять':
        print(f'Игрок берёт карту: {bot_answer_answer}')
        update.message.reply_text(f'Вы берёте карту {bot_answer_answer}')
        player.append(bot_answer_answer)
        n_player_cards += 1
        bot_move(update, context)
    elif answering == 'player' and card != 'взять':
        try:
            card = int(card)
        except ValueError:
            update.message.reply_text('Вы ввели не число!')
            return DEFINE_CARD

        print(f'Карта дефайн кард {card}')
        print(answering)

        try:
            if answering == 'bot':
                print(f'Выбранная карта: {player[card - 1]}')
                return player_move(update, context)
            elif answering == 'player':
                print(f'Выбранная для ответа карта: {player[card - 1]}')
                return player_answer(bot_answer_answer, update, context)

        except IndexError:
            update.message.reply_text('Вы ввели неправильное число или слово\n'
                                      'Попробуйте ещё раз.')

            return DEFINE_CARD


def login_password(update, context):
    global nik
    text = update.message.text
    con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
    cur = con.cursor()
    users = cur.execute("""SELECT nik FROM users_passwords""").fetchall()  # выбираем все данные из таблицы
    cur.close()
    users_s = []
    for i in users:
        users_s.append(i[0])
    users = users_s
    print(users)
    if text in users:
        update.message.reply_text('Привет ' + text + ' теперь введи свой пароль')
        nik = text
        return LOGIN_PASSWORD
    else:
        update.message.reply_text('Такого ника пока нет в моем списке, но я всегда рад новым знакомствам\n'
                                  'Теперь введи пароль с помощью которого ты будешь входить в аккаунт')
        nik = text
        return REGISTER


def login_password_one_more(update, context):
    global nik, money
    reply_keyboard = [['Карты'],
                      ['Монетка']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
    cur = con.cursor()
    passwords = cur.execute("""SELECT * FROM users_passwords""").fetchall()  # выбираем все данные из таблицы
    for j in passwords:
        if j[0] == nik:
            password = str(j[1])
    cur.close()
    password_here = update.message.text
    if password_here == password:
        con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
        cur = con.cursor()
        money = cur.execute("""SELECT * FROM money""").fetchall()  # выбираем все данные из таблицы
        for i in money:
            if i[0] == nik:
                money = i[1]
                break
        print(nik, money)
        cur.close()
        global already_started
        if already_started == 0:
            if int(money) >= 50:
                update.message.reply_text('Добро пожаловать в игру\n'
                                          'Будем играть в карты или в монетку?', reply_markup=markup)
                update.message.reply_text('Ваш баланс: ' + str(money))
                already_started = 1
                return DEFINE
            else:
                update.message.reply_text('На вашем балансе недостаточно средств для игры \n'
                                          'Возвращайтесь позже(((')
        else:
            update.message.reply_text('Игра уже началась! Введите /stop если хотите закончить\n'
                                      'и начать заново')
    else:
        update.message.reply_text('Пароль неверный')
        return LOGIN_PASSWORD


def register(update, context):
    global nik, users_dict, users, money
    text = update.message.text
    if text != '':
        update.message.reply_text('Наверное у тебя очень крутой пароль \n'
                                  'Жаль что я никогда не смогу его увидеть \n'
                                  'Ведь все пароли пользователей лежат в зашифрованных базах данных')
        update.message.reply_text('Пока не забыл: За регистрацию я начислил тебе 150 монет \n'
                                  'На монеты можно играть в карты! Одна игра это 50 монет! \n'
                                  'Победил - забрал 100. Проиграл - забрал 0')
        con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
        cursor = con.cursor()
        sqlite_insert_query = """INSERT INTO users_passwords VALUES ('""" + nik + "', '" + str(text) + "')"
        count = cursor.execute(
            sqlite_insert_query)  # добавляем в таблицу пользователей и их счета пользователя и счет
        con.commit()
        cursor.close()
        con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
        cursor = con.cursor()
        sqlite_insert_query = """INSERT INTO money VALUES ('""" + nik + "', '" + '150' + "')"
        count = cursor.execute(
            sqlite_insert_query)  # добавляем в таблицу пользователей и их счета пользователя и счет
        con.commit()
        cursor.close()

        global already_started
        if already_started == 0:
            update.message.reply_text('Добро пожаловать в игру\n'
                                      'Будем играть в карты или в монетку?\n'
                                      '<карты> или <монетка>')
            already_started = 1
            return DEFINE
        else:
            update.message.reply_text('Игра уже началась! Введите /stop если хотите закончить\n'
                                      'и начать заново')


def coin(update, context):
    global money
    reply_keyboard = [['Орел'],
                      ['Решка']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    if int(money) < 50:
        update.message.reply_text('К сожалению у вас недостаточно монет для игры в монетку')
        return DEFINE
    else:
        update.message.reply_text('Выберите сторону монетки\n'
                                  'Если хотите выйти из монетки напишите <выход>',
                                  reply_markup=markup)
        return COIN


def flip(update, context):
    global money, money_game
    reply_keyboard = [['Орел'],
                      ['Решка']]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    side = update.message.text
    if side.lower() != 'орел' and side.lower() != 'выход' and side.lower() != 'решка':
        coin(update, context)
    else:
        if int(money) < 50:
            update.message.reply_text('К сожалению у вас недостаточно монет для игры в монетку')
            return DEFINE
        else:
            if side.lower() == 'орел':
                side = '1'
            elif side.lower() == 'выход':
                update.message.reply_text('Вы вышли из игры в монетку \n'
                                          'Если хотите вернуться обратно, то напишите <монетка> \n'
                                          'Если хотите поиграть в карты напишите <карты>',
                                          reply_markup=ReplyKeyboardRemove())
                money_game = False
                return DEFINE
            else:
                side = '2'
            response = requests.post(
                'https://www.random.org/integers/?num=1&min=1&max=2&col=1&base=10&format=plain&rnd=new')
            if str(response.text)[0] == side:
                update.message.reply_text('Вы выиграли', reply_markup=markup)
                money = str(int(money) + 50)
            else:
                update.message.reply_text('Вы проиграли', reply_markup=markup)
                money = str(int(money) - 50)

            update.message.reply_text('Ваш баланс: ' + str(money))
            sqlite_connection = sqlite3.connect('ananas_bd.sqlite')  # импортируем базу данных
            cursor = sqlite_connection.cursor()
            sqlite_insert_query = cursor.execute("""DELETE FROM money
                WHERE nik = ?""", (nik,)).fetchall()
            sqlite_connection.commit()
            cursor.close()
            con = sqlite3.connect("ananas_bd.sqlite")  # импортируем базу данных
            cursor = con.cursor()
            sqlite_insert_query = """INSERT INTO money VALUES ('""" + nik + "', '" + str(money) + "')"
            count = cursor.execute(
                sqlite_insert_query)  # добавляем в таблицу пользователей и их счета пользователя и счет
            con.commit()
            cursor.close()


def defining_command(update, context):
    global already_started, money_game, card_game
    command = update.message.text
    print(command)

    if money_game is False and card_game is False:
        if command.lower() == 'карты':
            card_game = True
            print('\nНачало игры в карты')
            return game(update, context)

        elif command.lower() == 'монетка':
            print('\nНачало игры в монетку')
            money_game = True
            return coin(update, context)

    else:
        if command == 'Посмотреть карты':
            print('\nПросмотр карт')
            return show_cards(update, context)

        elif command == 'Управление':
            print('\nУправление')
            return controls(update, context)

        elif command == 'Сделать ход':
            print('\nХод игрока')
            return player_choose_card(update, context)

        elif command == 'Выход':
            print('\nВыход')
            already_started = 0
            return stop(update, context)


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', go)],
        states={
            DEFINE: [MessageHandler(Filters.text & ~Filters.command, defining_command)],
            DEFINE_CARD: [MessageHandler(Filters.text & ~Filters.command, define_card)],
            LOGIN_NIKNAME: [MessageHandler(Filters.text & ~Filters.command, login_password)],
            LOGIN_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, login_password_one_more)],
            REGISTER: [MessageHandler(Filters.text & ~Filters.command, register)],
            START: [MessageHandler(Filters.text & ~Filters.command, go)],
            COIN: [MessageHandler(Filters.text & ~Filters.command, flip)]
        },
        fallbacks=[CommandHandler('stop', stop), CommandHandler('controls', controls),
                   CommandHandler('show_cards', show_cards), CommandHandler('player_choose_card', player_choose_card),
                   CommandHandler('player_choose_answer', player_choose_answer)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()