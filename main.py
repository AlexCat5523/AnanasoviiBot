from colorama import init, Fore
import telegram
from telegram.ext import Updater, MessageHandler, Filters, ExtBot
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import CallbackQuery, ReplyKeyboardRemove, PhotoSize, Chat, Message
import random
import math
from time import sleep
import sys
import sqlite3
import requests
import json

updater = Updater('5102501109:AAEq0uyJj_Gy4pb3QbyHQMjzU7ayV26Q7iE', use_context=True)
telegram_bot = telegram.Bot(token='5102501109:AAEq0uyJj_Gy4pb3QbyHQMjzU7ayV26Q7iE')

# ВСЕ НОВЫЕ КОМАНДЫ ЗАСОВЫВАТЬ В FALLBACKS!!!
# Через них возвращать DEFINE, из-за чего процесс распознавания команд будет непрерывным и игра не завершится!

dp = updater.dispatcher
con = sqlite3.connect("ananas_bd.sqlite", check_same_thread=False)  # импортируем базу данных
cur = con.cursor()
money = cur.execute("""SELECT * FROM money""").fetchall()  # выбираем все данные из таблицы

print(f'Что такое {money}')

init()
running = True
cards_game = False  # начала игры в карты
sure = False    # выходим или нет
bot_take_card = False
show_weather = False

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

DEFINE, DEFINE_CARD, DEFINE_PLAYER_ANSWER, LOGIN_NIKNAME, LOGIN_PASSWORD, START, REGISTER, \
COIN, EXIT_DURING_MOVES = range(9)

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
nik = ''

koloda_forever = ['Туз_BUB', 'Король_BUB', 'Дама_BUB', 'Валет_BUB', 'Десять_BUB', 'Девять_BUB', 'Восемь_BUB',
                  'Семь_BUB', 'Шесть_BUB',
                  'Туз_PIK', 'Король_PIK', 'Дама_PIK', 'Валет_PIK', 'Десять_PIK', 'Девять_PIK', 'Восемь_PIK',
                  'Семь_PIK', 'Шесть_PIK',
                  'Туз_CHER', 'Король_CHER', 'Дама_CHER', 'Валет_CHER', 'Десять_CHER', 'Девять_CHER', 'Восемь_CHER',
                  'Семь_CHER', 'Шесть_CHER',
                  'Туз_TRE', 'Король_TRE', 'Дама_TRE', 'Валет_TRE', 'Десять_TRE', 'Девять_TRE', 'Восемь_TRE',
                  'Семь_TRE', 'Шесть_TRE']

# geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"  # геокодер (для нахождения положения)


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

    if first_turn == '':
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
        if first_turn == 'player':
            print('ПЕРВЫЙ ХОДИТ ИГРОК')
        else:
            print('ПЕРВЫЙ ХОДИТ БОТ')


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
    global n_bot_cards, n_player_cards, cozir_flag, card, answering, bot_take_card
    answering = 'bot'
    print(f'Карта плэйер мува {card}')
    move = True

    while move:
        answ = player[card - 1]
        n_player_cards -= 1

        if n_player_cards == 0:     # если число карт == 0
            update.message.reply_text('Вы молодец!')
            return pobeda('p', update, context)

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
        if bot_take_card:
            player_choose_card(update, context)
            bot_take_card = False
        else:
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

    if n_bot_cards == 0:    # победа бота
        update.message.reply_text('БОТ ВЫИГРАЛ')
        return pobeda('b', update, context)
    else:
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
    global n_bot_cards, answering
    bot.append(carta)
    n_bot_cards += 1
    answering = 'bot'


def bot_answ(update, context, movek):
    global bot, vel_card, cozir, n_player_cards, n_bot_cards, cozir_flag, answering, bot_take_card
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
            bot_take_card = True
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
    global first_turn, cards_game
    if cards_game is True:
        giving_cards(6, update, context)
        if first_turn == 'player':
            controls(update, context)
        elif first_turn == 'bot':
            print('Бот ходит')
#            bot_move(update, context)


def pobeda(who_wins, update, context):
    global money, cards_game, player, bot, koloda_forever, koloda, sure

    if who_wins == 'p':
        update.message.reply_text('МОЛОДЕЦ')
        sqlite_connection = sqlite3.connect('ananas_bd.sqlite')  # импортируем базу данных
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = cursor.execute("""DELETE from money
        where nik = ?""", (nik, )).fetchall()
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

        koloda = koloda_forever
        player.clear()
        bot.clear()
        cards_game = False
        sure = False
        return DEFINE

    if who_wins == 'b':
        update.message.reply_text('НЕ ПОВЕЗЛО? ПОПРОБУЙ ЕЩЕ РАЗ')
        sqlite_connection = sqlite3.connect('ananas_bd.sqlite')  # импортируем базу данных
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = cursor.execute("""DELETE from money
        where nik = ?""", (nik, )).fetchall()
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

        koloda = koloda_forever
        player.clear()
        bot.clear()
        cards_game = False
        sure = False
        return DEFINE


def stop(update, context):
    global already_started
#    already_started = 0
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
    update.message.reply_text('Здравствуйте! Пожалуйста войдите в свой аккаунт или зарегистрируйтесь')
    update.message.reply_text('Введите свой никнейм')
    return LOGIN_NIKNAME


def exit_during_moves(update, context):
    global cards_game, sure
    answer = update.message.text
    print(f'Ответ во время выхода: {answer}')

    if answer.lower() == 'да':
        print(f'Выходим во время игры...')
        update.message.reply_text('Вы вышли из карт')
        sure = False
        cards_game = False
        select_money = cur.execute('''SELECT money FROM money WHERE nik = ?''', (nik,)).fetchall()
        print(select_money)

        for i in select_money:
            for j in i:
                update_value = cur.execute('''UPDATE money SET money = ? WHERE nik = ?''',
                                           (int(j) - 50, nik)).fetchall()
                con.commit()

        update.message.reply_text('\nВы вышли из карт'
                                  '\nВведите <карты> или <монетка> для игры')
        koloda = koloda_forever
        player.clear()
        bot.clear()
        return DEFINE

    elif answer.lower() == 'нет':
        update.message.reply_text('Вы не вышли из карт')
        sure = False


def define_card(update, context):
    global card, answering, n_player_cards, player
    card = update.message.text      # получаем сообщение из player_choose_card
    print(f'Здесь начинается дефайн кард!')

    if answering == 'player' and card == 'взять':
        print(f'Игрок берёт карту: {bot_answer_answer}')
        update.message.reply_text(f'Вы берёте карту {bot_answer_answer}')
        player.append(bot_answer_answer)
        n_player_cards += 1
        bot_move(update, context)
    else:
        if card.lower() == 'выход':
            update.message.reply_text('Вы уверены что хотите выйти?'
                                      '\nВаши 50 очков не сохранятся')
            return EXIT_DURING_MOVES
        else:
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
                      ['Монетка'],
                      ['Посмотреть погоду']]
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
                                          'Будем играть в карты или в монетку?'
                                          '\nА может быть хочешь узнать погоду?', reply_markup=markup)
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
                                      'Может посмотрим погоду?')
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
    global money
    reply_keyboard = [['Орел'],
                      ['Решка']]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    side = update.message.text
    photo_answer = ''
    chat_id = update.message.chat.id
    if side.lower() != 'орел' and side.lower() != 'выход' and side.lower() != 'решка':
        coin(update, context)
    else:
        if int(money) < 50:
            update.message.reply_text('К сожалению у вас недостаточно монет для игры в монетку')
            return DEFINE
        else:
            if side.lower() == 'орел':
                side = '1'
                photo_answer = 'img/1'
            elif side.lower() == 'выход':
                update.message.reply_text('Вы вышли из игры в монетку \n'
                                          'Если хотите вернуться обратно, то напишите <монетка> \n'
                                          'Если хотите поиграть в карты напишите <карты>',
                                          reply_markup=ReplyKeyboardRemove())
                
                return DEFINE
            else:
                side = '2'
                photo_answer = 'img/2'
            response = requests.post(
                'https://www.random.org/integers/?num=1&min=1&max=2&col=1&base=10&format=plain&rnd=new')
            if str(response.text)[0] == side:
                photo_answer = f'{photo_answer}_win.jpg'  # фото
                telegram_bot.send_photo(chat_id, open(photo_answer, 'rb'))
                update.message.reply_text('Вы выиграли',
                                          reply_markup=markup)
                money = str(int(money) + 50)
            else:
                photo_answer = f'img/{str(response.text)[0]}_defeat.jpg'
                telegram_bot.send_photo(chat_id, open(photo_answer, 'rb'))
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


def users_output(update, context):  # для обработки ввода для магнита и т.п
    global show_weather
    show_weather = True
    return DEFINE


def find_weather(update, context, city):
    forecast_api = 'e9d384fccd160b5870e32f1deb7cd3b8'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={forecast_api}&lang=ru'
    response = requests.get(url)
    json_response = response.json()
    temperature = json_response['main']['temp']
    temperature = round(temperature - 273.1, 1)

    if json_response['weather'][0]['main'] == 'Clouds':
        update.message.reply_text(f'Облачно, но можно пойти в магазинчик. '
                                  f'\nТемпература: {temperature} \u2103')
    elif json_response['weather'][0]['main'] == 'Rain':
        update.message.reply_text(f'Дождь, лучше остаться доме. '
              f'\nТемпература: {temperature} \u2103')
    elif json_response['weather'][0]['main'] == 'Clear':
        update.message.reply_text(f'Солнечно, надо идти в магазинчик. '
              f'\nТемпература: {temperature} \u2103')
    elif json_response['weather'][0]['main'] == 'Snow':
        update.message.reply_text(f'Снег, но можно сходить в магазин. '
              f'\nТемпература: {temperature} \u2103')

    return DEFINE


def defining_command(update, context):
    global already_started, cards_game, koloda, koloda_forever, player, bot, nik, sure, show_weather
    command = update.message.text
    print(f'Команда: {command}')

    if command.lower() == 'карты':
        print('\nНачало игры в карты')
        cards_game = True
        return game(update, context)

    elif command.lower() == 'монетка':
        print('\nНачало игры в монетку')

        return coin(update, context)

    elif command.lower() == 'посмотреть погоду':
        update.message.reply_text('Введите своё местоположение (с улицей и адресом) в формате:'
                                  '\nСочи, улица Горького, 44')
        return users_output(update, context)

    elif command.lower() == 'выход':
        if cards_game is False and show_weather is False:
            print('\nВыход')
            already_started = 0
            return stop(update, context)
        elif show_weather is True:
            print('\nВыход из погоды')
            update.message.reply_text('Вы вышли из просмотра погоды')
            show_weather = False
            return DEFINE
        else:
            print('\nВыход из карт')
            update.message.reply_text('\nВы уверены что хотите выйти?'
                                      '\nВаши 50 монет не сохранятся')
            sure = True
            return DEFINE

    elif show_weather is True:
        if command.lower() != 'выход' and command.isdigit() is False:
            return find_weather(update, context, command)
        else:
            if command.isdigit() is True:
                update.message.reply_text('Вы ввели число!'
                                          '\nВведите запрос заново или введите <выход>')
                return users_output(update, context)    # может появиться ошибка с двумя сообщениями

    elif cards_game is True and sure is True:
        if command.lower() == 'да':
            cards_game = False
            sure = False
            select_money = cur.execute('''SELECT money FROM money WHERE nik = ?''', (nik, )).fetchall()
            print(select_money)

            for i in select_money:
                for j in i:
                    update_value = cur.execute('''UPDATE money SET money = ? WHERE nik = ?''', (int(j) - 50, nik)).fetchall()
                    con.commit()

            update.message.reply_text('\nВы вышли из карт'
                                      '\nВведите <карты> или <монетка> для игры')
            koloda = koloda_forever
            player.clear()
            bot.clear()
            return DEFINE

        elif command.lower() == 'нет':
            update.message.reply_text('Вы не вышли из карт')
            sure = False

    if cards_game is True:
        if command.lower() == 'посмотреть карты':
            print('\nПросмотр карт')
            return show_cards(update, context)

        elif command.lower() == 'управление':
            print('\nУправление')
            return controls(update, context)

        elif command.lower() == 'сделать ход':
            print('\nХод игрока')
            return player_choose_card(update, context)

        elif command == 'INSTANT_WIN':
            print('\nADMIN: мгновенная победа')
            return pobeda('b', update, context)


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
            COIN: [MessageHandler(Filters.text & ~Filters.command, flip)],
            EXIT_DURING_MOVES: [MessageHandler(Filters.text & ~Filters.command, exit_during_moves)]
        },
        fallbacks=[CommandHandler('stop', stop), CommandHandler('controls', controls),
                   CommandHandler('show_cards', show_cards), CommandHandler('player_choose_card', player_choose_card),
                   CommandHandler('player_choose_answer', player_choose_answer),
                   CommandHandler('users_output', users_output)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()