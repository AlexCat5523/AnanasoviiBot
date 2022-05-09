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


class Class_game:
    def __init__(self):

        # ВСЕ НОВЫЕ КОМАНДЫ ЗАСОВЫВАТЬ В FALLBACKS!!!
        # Через них возвращать DEFINE, из-за чего процесс распознавания команд будет непрерывным и игра не завершится!

        self.dp = updater.dispatcher
        self.con = sqlite3.connect("ananas_bd.sqlite", check_same_thread=False)  # импортируем базу данных
        self.cur = self.con.cursor()
        self.money = self.cur.execute("""SELECT * FROM money""").fetchall()  # выбираем все данные из таблицы

        print(f'Что такое {self.money}')

        self.running = True
        self.cards_game = False  # начала игры в карты
        self.sure = False  # выходим или нет
        self.bot_take_card = False
        self.show_weather = False
        self.cozir_flag = False

        self.cards_n = 36
        self.cards = ['PIK', 'TRE', 'CHER', 'BUB']
        self.card = 0  # выбор карты
        self.vel_card = {'Шесть': 1, 'Семь': 2, 'Восемь': 3, 'Девять': 4, 'Десять': 5, 'Валет': 6, 'Дама': 7,
                         'Король': 8, 'Туз': 9}

        self.n_player_cards = 6
        self.n_bot_cards = 6
        self.already_started = 0
        self.CARDS = {
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

        self.answering = ''  # отвечающий (ходит: игрок, отвечает: бот)
        self.bot_answer_answer = ''  # ответ бота на ход игрока (для того, чтобы можно было передавать по функциям)

        self.DEFINE, self.DEFINE_CARD, self.DEFINE_PLAYER_ANSWER, self.LOGIN_NIKNAME, self.LOGIN_PASSWORD, \
        self.START, self.REGISTER, self.COIN, self.EXIT_DURING_MOVES = range(9)

        self.player = list()
        self.bot = list()
        self.first_turn = ''  # можно поставить на player, чтобы он всегда начинал ходить первым
        self.cozir = ''
        self.koloda = ['Туз_BUB', 'Король_BUB', 'Дама_BUB', 'Валет_BUB', 'Десять_BUB', 'Девять_BUB', 'Восемь_BUB',
                       'Семь_BUB',
                       'Шесть_BUB',
                       'Туз_PIK', 'Король_PIK', 'Дама_PIK', 'Валет_PIK', 'Десять_PIK', 'Девять_PIK', 'Восемь_PIK',
                       'Семь_PIK',
                       'Шесть_PIK',
                       'Туз_CHER', 'Король_CHER', 'Дама_CHER', 'Валет_CHER', 'Десять_CHER', 'Девять_CHER',
                       'Восемь_CHER',
                       'Семь_CHER', 'Шесть_CHER',
                       'Туз_TRE', 'Король_TRE', 'Дама_TRE', 'Валет_TRE', 'Десять_TRE', 'Девять_TRE', 'Восемь_TRE',
                       'Семь_TRE',
                       'Шесть_TRE']
        self.nik = ''

        self.koloda_forever = ['Туз_BUB', 'Король_BUB', 'Дама_BUB', 'Валет_BUB', 'Десять_BUB', 'Девять_BUB',
                               'Восемь_BUB',
                               'Семь_BUB', 'Шесть_BUB',
                               'Туз_PIK', 'Король_PIK', 'Дама_PIK', 'Валет_PIK', 'Десять_PIK', 'Девять_PIK',
                               'Восемь_PIK',
                               'Семь_PIK', 'Шесть_PIK',
                               'Туз_CHER', 'Король_CHER', 'Дама_CHER', 'Валет_CHER', 'Десять_CHER', 'Девять_CHER',
                               'Восемь_CHER',
                               'Семь_CHER', 'Шесть_CHER',
                               'Туз_TRE', 'Король_TRE', 'Дама_TRE', 'Валет_TRE', 'Десять_TRE', 'Девять_TRE',
                               'Восемь_TRE',
                               'Семь_TRE', 'Шесть_TRE']

        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"  # геокодер (для нахождения положения)

    def show_cards(self, update, context):
        s = ''
        s += f'Козырь: {self.cozir}\n'
        s += f'Ваши карты: \n'
        for i in self.player:
            s += f'{self.player.index(i) + 1}: {i}\n'
        update.message.reply_text(s)

        return self.DEFINE

    def giving_cards(self, n, update, context):
        for i in range(n):
            card = random.choice(self.koloda)
            self.player.append(card)
            del self.koloda[self.koloda.index(card)]

        for i in range(n):
            card = random.choice(self.koloda)
            self.bot.append(card)
            del self.koloda[self.koloda.index(card)]

        self.cozir = random.choice(self.koloda)
        self.cozir_flag = True
        del self.koloda[self.koloda.index(self.cozir)]

        self.show_cards(update, context)
        min_bot = ''
        for card in self.bot:
            if card.split('_')[1] == self.cozir.split('_')[1]:
                if min_bot == '':
                    min_bot = card
                elif self.koloda_forever.index(card) > self.koloda_forever.index(min_bot):
                    min_bot = card
                else:
                    pass
            else:
                pass

        if min_bot != '':
            index_bot = self.koloda_forever.index(min_bot)
        else:
            index_bot = -1
        min_player = ''
        for card in self.player:
            if card.split('_')[1] == self.cozir.split('_')[1]:
                if min_player == '':
                    min_player = card
                elif self.koloda_forever.index(card) > self.koloda_forever.index(min_player):
                    min_player = card
                else:
                    pass
            else:
                pass

        if min_player != '':
            index_player = self.koloda_forever.index(min_player)
        else:
            index_player = -1

        if self.first_turn == '':
            if min_bot != '' and min_player != '':
                if index_player > index_bot:
                    self.first_turn = 'player'
                    print('ПЕРВЫЙ ХОДИТ ИГРОК')
                elif index_player < index_bot:
                    self.first_turn = 'bot'
                    print('ПЕРВЫЙ ХОДИТ БОТ')
            elif min_bot == '' and min_player != '':
                self.first_turn = 'player'
                print('ПЕРВЫЙ ХОДИТ ИГРОК')
            elif min_bot != '' and min_player == '':
                self.first_turn = 'bot'
                print('ПЕРВЫЙ ХОДИТ БОТ')
            else:
                self.first_turn = 'player'
                print('ПЕРВЫЙ ХОДИТ ИГРОК')
            self.cards_n = 23
        else:
            if self.first_turn == 'player':
                print('ПЕРВЫЙ ХОДИТ ИГРОК')
            else:
                print('ПЕРВЫЙ ХОДИТ БОТ')

    def exit(self):
        self.running = False
        return self.running

    def player_choose_card(self, update, context):
        update.message.reply_text('Выберите карту:')
        self.show_cards(update, context)
        self.answering = 'bot'

        return self.DEFINE_CARD

    def player_move(self, update, context):
        self.answering = 'bot'
        print(f'Карта плэйер мува {self.card}')
        move = True

        while move:
            answ = self.player[self.card - 1]
            self.n_player_cards -= 1

            if self.n_player_cards == 0:  # если число карт == 0
                update.message.reply_text('Вы молодец!')
                return self.pobeda('p', update, context)

            del self.player[self.player.index(self.player[self.card - 1])]

            if self.n_player_cards < 6:  # добавление карт if number of cards < 6
                if len(self.koloda) != 0:
                    self.card = random.choice(self.koloda)
                    self.player.append(self.card)
                    del self.koloda[self.koloda.index(self.card)]
                    self.n_player_cards += 1

                elif self.cozir_flag:
                    self.player.append(self.cozir)
                    self.cozir_flag = False
                    self.n_player_cards += 1

            self.bot_answ(update, context, answ)
            if self.bot_take_card:
                self.player_choose_card(update, context)
                self.bot_take_card = False
            else:
                update.message.reply_text('Теперь ходит бот')
                self.bot_move(update, context)
            move = False

    def player_answer(self, bot_hod, update, context):
        Flag = False
        move = True
        self.answering = 'player'
        print(f'Карта ансвера {self.card}')

        while move:
            if self.player[self.card - 1].split('_')[1] != self.cozir.split('_')[1]:
                if bot_hod.split('_')[1] == self.player[self.card - 1].split('_')[1]:
                    if self.vel_card[self.player[self.card - 1].split('_')[0]] > self.vel_card[bot_hod.split('_')[0]]:
                        player_answ = self.player[self.card - 1]
                        Flag = True
                    else:
                        update.message.reply_text('Выбранная вами карта не побивает ' + bot_hod)
                        return self.player_choose_answer(self.bot_answer_answer, update, context)
                else:
                    update.message.reply_text('Выбранная вами карта не побивает ' + bot_hod)
                    return self.player_choose_answer(self.bot_answer_answer, update, context)

            elif bot_hod.split('_')[1] != self.cozir.split('_')[1]:
                Flag = True
                player_answ = self.player[self.card - 1]

            else:
                if self.vel_card[self.player[self.card - 1].split('_')[0]] > self.vel_card[bot_hod.split('_')[0]]:
                    player_answ = self.player[self.card - 1]
                    Flag = True
                else:
                    update.message.reply_text('Выбранная вами карта не побивает ' + bot_hod)

            if Flag:
                update.message.reply_text('Вы побили ' + bot_hod + ' картой ' + player_answ)
                del self.player[self.card - 1]
                self.n_player_cards -= 1

                if self.n_player_cards == 0:  # победа игрока
                    print('ВЫ ВЫИГРАЛИ')
                    self.pobeda(self, 'p', update, context)

                if self.n_player_cards < 6:  # раздача карт
                    if len(self.koloda) != 0:
                        self.card = random.choice(self.koloda)
                        self.player.append(self.card)
                        del self.koloda[self.koloda.index(self.card)]
                        self.n_player_cards += 1
                    elif self.cozir_flag:
                        self.player.append(self.cozir)
                        self.cozir_flag = False
                        self.n_player_cards += 1

                move = False
                update.message.reply_text('Теперь ваш ход, удачи')
                self.player_choose_card(update, context)

    def player_choose_answer(self, bot_hod, update, context):
        update.message.reply_text('Чем ответим?')
        self.show_cards(update, context)
        update.message.reply_text('Напишите <взять>, если хотите взять')
        self.answering = 'player'
        self.bot_answer_answer = bot_hod
        print(f'Ход бота: {self.bot_answer_answer} в choose_answer')

        return self.DEFINE_CARD

    def bot_move(self, update, context):
        spisok_card = {'Шесть': [], 'Семь': [], 'Восемь': [], 'Девять': [], 'Десять': [], 'Валет': [], 'Дама': [],
                       'Король': [], 'Туз': []}
        answ = []
        self.answering = 'player'

        if self.n_bot_cards == 0:  # победа бота
            update.message.reply_text('БОТ ВЫИГРАЛ')
            return pobeda(self, 'b', update, context)
        else:
            for i in self.bot:
                if len(self.koloda) > 0:
                    if i.split('_')[1] == self.cozir.split('_')[1]:
                        pass
                    else:
                        spisok_card[i.split('_')[0]].append(i)
                else:
                    spisok_card[i.split('_')[0]].append(i)

            for i in spisok_card.keys():
                if not answ:
                    if len(spisok_card[i]) >= 2:
                        answ = spisok_card[i]
                    elif len(answ) < 2 and bool(spisok_card[i]):
                        answ = spisok_card[i]

            print(f'\nБот атакует {answ[0]}')
            del self.bot[self.bot.index(answ[0])]
            self.n_bot_cards -= 1

            if self.n_bot_cards < 6:
                if len(self.koloda) != 0:
                    card = random.choice(self.koloda)
                    self.bot.append(card)
                    del self.koloda[self.koloda.index(card)]
                    self.n_bot_cards += 1

                elif self.cozir_flag:
                    self.bot.append(self.cozir)
                    self.cozir_flag = False
                    self.n_bot_cards += 1

            # print(f'Ошибка от бота: {answ[0]}, {type(answ[0])}')
            update.message.reply_text('Бот атакует: ' + answ[0])
            return self.player_choose_answer(answ[0], update, context)

    def bot_taking_cards(self, carta, update, context):
        self.bot.append(carta)
        self.n_bot_cards += 1
        self.answering = 'bot'

    def bot_answ(self, update, context, movek):
        self.answering = 'bot'
        answ = ''
        print(f'\nКарты бота: {self.bot}')

        for i in self.bot:
            if i.split('_')[1] == movek.split('_')[1]:
                if answ == '':
                    if self.vel_card[movek.split('_')[0]] > self.vel_card[i.split('_')[0]]:
                        pass
                    else:
                        answ = i
                else:
                    if self.vel_card[movek.split('_')[0]] > self.vel_card[i.split('_')[0]]:
                        pass
                    elif self.vel_card[i.split('_')[0]] > self.vel_card[answ.split('_')[0]]:
                        answ = i
        if answ != '':
            print(f'Ответ бота: {answ}')
            update.message.reply_text(f'Ответ бота: {answ}')
            del self.bot[self.bot.index(answ)]
            self.n_bot_cards -= 1

            if self.n_bot_cards == 0:
                update.message.reply_text('Бот победил!')
                self.pobeda('b', update, context)

            if self.n_bot_cards < 6:
                if len(self.koloda) != 0:
                    card = random.choice(self.koloda)
                    self.bot.append(card)
                    del self.koloda[self.koloda.index(card)]
                    self.n_bot_cards += 1
                elif self.cozir_flag:
                    self.bot.append(self.cozir)
                    self.cozir_flag = False
                    self.n_bot_cards += 1
        else:
            if len(self.koloda) > 5:
                pass
            elif movek.split('_')[1] != self.cozir.split('_')[1]:
                for i in bot:
                    if answ == '':
                        answ = i
                    else:
                        if self.vel_card[i.split('_')[0]] > self.vel_card[answ.split('_')[0]]:
                            answ = i
                        else:
                            pass
            if answ == '':
                update.message.reply_text('Бот не может отбиться, бот принимает')
                self.bot_take_card = True
                return self.bot_taking_cards(movek, update, context)  # здесь начинается ошибка

            else:
                update.message.reply_text('Бот бьет ' + movek + ' картой ' + answ)
                del self.bot[self.bot.index(answ)]
                self.n_bot_cards -= 1

                if self.n_bot_cards == 0:
                    update.message.reply_text('Бот победил!')
                    self.pobeda('b', update, context)

                if self.n_bot_cards < 6:
                    if len(self.koloda) != 0:
                        card = random.choice(self.koloda)
                        self.bot.append(card)
                        del self.koloda[self.koloda.index(card)]
                        self.n_bot_cards += 1

                    elif self.cozir_flag:
                        self.bot.append(self.cozir)
                        self.cozir_flag = False
                        self.n_bot_cards += 1

    def game(self, update, context):
        if self.cards_game is True:
            self.giving_cards(6, update, context)
            if self.first_turn == 'player':
                self.controls(update, context)
            elif self.first_turn == 'bot':
                print('Бот ходит')
                self.controls(update, context)

    def pobeda(self, who_wins, update, context):
        if who_wins == 'p':
            update.message.reply_text('МОЛОДЕЦ')

            select_money = self.cur.execute('''SELECT money FROM money WHERE nik = ?''', (self.nik,)).fetchall()
            for i in select_money:
                self.cur.execute('''UPDATE money SET money = ? WHERE nik = ?''', (int(i[0]), self.nik,))
                self.cur.close()
            money = str(int(self.money) + 50)
            update.message.reply_text('Ваш баланс: ' + str(self.money))

            self.koloda = koloda_forever
            self.player.clear()
            self.bot.clear()
            self.cards_game = False
            self.sure = False
            return self.DEFINE

        if who_wins == 'b':
            update.message.reply_text('НЕ ПОВЕЗЛО? ПОПРОБУЙ ЕЩЕ РАЗ')
            sqlite_insert_query = self.cur.execute("""DELETE from money
            where nik = ?""", (self.nik,)).fetchall()  # исполнение команды
            self.con.commit()

            sqlite_insert_query2 = """INSERT INTO money VALUES ('""" + self.nik + "', '" + str(
                int(self.money) - 50) + "')"
            count = self.cur.execute(
                sqlite_insert_query2)  # добавляем в таблицу пользователей и их счета пользователя и счет
            self.con.commit()

            self.money = str(int(self.money) - 50)
            update.message.reply_text('Ваш баланс: ' + str(self.money))

            self.koloda = self.koloda_forever
            self.player.clear()
            self.bot.clear()
            self.cards_game = False
            self.sure = False
            return self.DEFINE

    def stop(self, update, context):
        self.already_started = 0
        update.message.reply_text('Выходим...', reply_markup=ReplyKeyboardRemove())
        select_money = self.cur.execute('''SELECT money FROM money WHERE nik = ?''', (self.nik,)).fetchall()
        if self.cards_game:
            for i in select_money:
                for j in i:
                    self.cur.execute('''UPDATE money SET money = ? WHERE nik = ?''', (int(j) - 50, self.nik))
                    self.con.commit()
                    self.cards_game = False
        return ConversationHandler.END

    def controls(self, update, context):
        if self.first_turn == 'player':
            reply_keyboard = [['Посмотреть карты', 'Сделать ход'],
                              ['Управление', 'Выход']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text('Что вы хотите сделать?',
                                      reply_markup=markup)
        else:
            reply_keyboard = [['Посмотреть карты', 'Начать игру'],
                              ['Управление', 'Выход']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            update.message.reply_text('Что вы хотите сделать?',
                                      reply_markup=markup)

        return self.DEFINE

    def go(self, update, context):
        update.message.reply_text('Здравствуйте! Пожалуйста войдите в свой аккаунт или зарегистрируйтесь')
        update.message.reply_text('Введите свой никнейм')
        return self.LOGIN_NIKNAME

    def exit_during_moves(self, update, context):
        answer = update.message.text
        print(f'Ответ во время выхода: {answer}')

        if answer.lower() == 'да':
            print(f'Выходим во время игры...')
            update.message.reply_text('Вы вышли из карт')
            self.sure = False
            self.cards_game = False
            select_money = self.cur.execute('''SELECT money FROM money WHERE nik = ?''', (self.nik,)).fetchall()
            print(select_money)

            for i in select_money:
                for j in i:
                    update_value = self.cur.execute('''UPDATE money SET money = ? WHERE nik = ?''',
                                               (int(j) - 50, self.nik)).fetchall()
                    self.con.commit()

            update.message.reply_text('\nВы вышли из карт'
                                      '\nВведите <карты> или <монетка> для игры')
            self.koloda = self.koloda_forever
            self.player.clear()
            self.bot.clear()
            return self.DEFINE

        elif answer.lower() == 'нет':
            update.message.reply_text('Вы не вышли из карт')
            self.sure = False

    def define_card(self, update, context):
        card = update.message.text  # получаем сообщение из player_choose_card
        print(f'Здесь начинается дефайн кард!')

        if self.answering == 'player' and card == 'взять':
            print(f'Игрок берёт карту: {self.bot_answer_answer}')
            update.message.reply_text(f'Вы берёте карту {self.bot_answer_answer}')
            self.player.append(self.bot_answer_answer)
            self.n_player_cards += 1
            self.bot_move(update, context)
        else:
            if card.lower() == 'выход':
                update.message.reply_text('Вы уверены что хотите выйти?'
                                          '\nВаши 50 очков не сохранятся')
                return self.EXIT_DURING_MOVES
            else:
                try:
                    card = int(card)
                    self.card = card
                except ValueError:
                    update.message.reply_text('Вы ввели не число!')
                    return self.DEFINE_CARD

            print(f'Карта дефайн кард {card}')

            try:
                if self.answering == 'bot':
                    print(f'Выбранная карта: {self.player[card - 1]}')
                    return self.player_move(update, context)

                elif self.answering == 'player':
                    print(f'Выбранная для ответа карта: {self.player[card - 1]}')
                    return self.player_answer(self.bot_answer_answer, update, context)

            except IndexError:
                update.message.reply_text('Вы ввели неправильное число или слово\n'
                                          'Попробуйте ещё раз.')

                return self.DEFINE_CARD

    def login_password(self, update, context):
        text = update.message.text
        users = self.cur.execute("""SELECT nik FROM users_passwords""").fetchall()  # выбираем все данные из таблицы

        users_s = []
        for i in users:
            users_s.append(i[0])
        users = users_s
        print(users)
        if text in users:
            update.message.reply_text('Привет ' + text + ' теперь введи свой пароль')
            self.nik = text
            return self.LOGIN_PASSWORD
        else:
            update.message.reply_text('Такого ника пока нет в моем списке, но я всегда рад новым знакомствам\n'
                                      'Теперь введи пароль с помощью которого ты будешь входить в аккаунт')
            self.nik = text
            return self.REGISTER

    def login_password_one_more(self, update, context):
        reply_keyboard = [['Карты'],
                          ['Монетка'],
                          ['Посмотреть погоду']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        passwords = self.cur.execute("""SELECT * FROM users_passwords""").fetchall()  # выбираем все данные из таблицы
        money = 0
        for j in passwords:
            if j[0] == self.nik:
                password = str(j[1])

        password_here = update.message.text
        if password_here == password:
            money = self.cur.execute("""SELECT money FROM money WHERE nik = ?""", (self.nik,)).fetchall()  # выбираем все данные из таблицы

            for i in money:
                for j in i:
                    self.money = j

            if self.already_started == 0:
                if int(self.money) >= 50:
                    update.message.reply_text('Добро пожаловать в игру\n'
                                              'Будем играть в карты или в монетку?'
                                              '\nА может быть хочешь узнать погоду?', reply_markup=markup)
                    update.message.reply_text('Ваш баланс: ' + str(self.money))
                    self.already_started = 1
                    return self.DEFINE
                else:
                    update.message.reply_text('На вашем балансе недостаточно средств для игры \n'
                                              'Возвращайтесь позже(((')
            else:
                update.message.reply_text('Игра уже началась! Введите /stop если хотите закончить\n'
                                          'и начать заново')
        else:
            update.message.reply_text('Пароль неверный')
            return self.LOGIN_PASSWORD

    def register(self, update, context):
        text = update.message.text
        if text != '':
            update.message.reply_text('Наверное у тебя очень крутой пароль \n'
                                      'Жаль что я никогда не смогу его увидеть \n'
                                      'Ведь все пароли пользователей лежат в зашифрованных базах данных')
            update.message.reply_text('Пока не забыл: За регистрацию я начислил тебе 150 монет \n'
                                      'На монеты можно играть в карты! Одна игра это 50 монет! \n'
                                      'Победил - забрал 100. Проиграл - забрал 0')
            sqlite_insert_query = """INSERT INTO users_passwords VALUES ('""" + self.nik + "', '" + str(text) + "')"
            count = self.cur.execute(
                sqlite_insert_query)  # добавляем в таблицу пользователей и их счета пользователя и счет
            self.con.commit()

            sqlite_insert_query2 = """INSERT INTO money VALUES ('""" + self.nik + "', '" + '150' + "')"
            count = self.cur.execute(
                sqlite_insert_query2)  # добавляем в таблицу пользователей и их счета пользователя и счет
            self.con.commit()

            if self.already_started == 0:
                update.message.reply_text('Добро пожаловать в игру\n'
                                          'Будем играть в карты или в монетку?\n'
                                          'Может посмотрим погоду?')
                self.already_started = 1
                return self.DEFINE
            else:
                update.message.reply_text('Игра уже началась! Введите /stop если хотите закончить\n'
                                          'и начать заново')

    def coin(self, update, context):
        reply_keyboard = [['Орел'],
                          ['Решка']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        if int(self.money) < 50:
            update.message.reply_text('К сожалению у вас недостаточно монет для игры в монетку')
            return self.DEFINE
        else:
            update.message.reply_text('Выберите сторону монетки\n'
                                      'Если хотите выйти из монетки напишите <выход>',
                                      reply_markup=markup)
            return self.COIN

    def flip(self, update, context):
        reply_keyboard = [['Орел'],
                          ['Решка']]
        markup = ReplyKeyboardMarkup(reply_keyboard)
        side = update.message.text
        photo_answer = ''
        chat_id = update.message.chat.id
        if side.lower() != 'орел' and side.lower() != 'выход' and side.lower() != 'решка':
            self.coin(update, context)
        else:
            if int(self.money) < 50:
                update.message.reply_text('К сожалению у вас недостаточно монет для игры в монетку')
                return self.DEFINE
            else:
                if side.lower() == 'орел':
                    side = '1'
                    photo_answer = 'img/1'
                elif side.lower() == 'выход':
                    update.message.reply_text('Вы вышли из игры в монетку \n'
                                              'Если хотите вернуться обратно, то напишите <монетка> \n'
                                              'Если хотите поиграть в карты напишите <карты>',
                                              reply_markup=ReplyKeyboardRemove())

                    return self.DEFINE
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
                    self.money = str(int(self.money) + 50)
                else:
                    photo_answer = f'img/{str(response.text)[0]}_defeat.jpg'
                    telegram_bot.send_photo(chat_id, open(photo_answer, 'rb'))
                    update.message.reply_text('Вы проиграли', reply_markup=markup)
                    self.money = str(int(self.money) - 50)

                update.message.reply_text('Ваш баланс: ' + str(self.money))
                sqlite_insert_query = self.cur.execute("""UPDATE money SET money = ? WHERE nik = ?""", (self.money,
                                                                                                        self.nik,)).fetchall()
                self.con.commit()

    def users_output(self):  # для обработки ввода для погоды и т.п
        self.show_weather = True
        return self.DEFINE

    def find_weather(self, update, city):
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
            update.message.reply_text(f'Дождь, лучше остаться дома. '
                                      f'\nТемпература: {temperature} \u2103')
        elif json_response['weather'][0]['main'] == 'Clear':
            update.message.reply_text(f'Солнечно, надо идти в магазинчик. '
                                      f'\nТемпература: {temperature} \u2103')
        elif json_response['weather'][0]['main'] == 'Snow':
            update.message.reply_text(f'Снег, но можно сходить в магазин. '
                                      f'\nТемпература: {temperature} \u2103')

        self.show_weather = False
        return self.DEFINE

    def defining_command(self, update, context):
        command = update.message.text
        print(f'Команда: {command}')

        if not self.cards_game:
            select_money = self.cur.execute('''SELECT money FROM money WHERE nik = ?''', (self.nik,)).fetchall()
            for i in select_money:
                if int(i[0]) < 50:
                    update.message.reply_text('Ваш баланс: 0'
                                              '\nАвтоматический выход из бота')
                    return self.stop(update, context)
            if command.lower() == 'карты':
                print('\nНачало игры в карты')
                self.cards_game = True
                return self.game(update, context)

            elif command.lower() == 'монетка':
                print('\nНачало игры в монетку')
                return self.coin(update, context)

            elif command.lower() == 'посмотреть погоду':
                update.message.reply_text('Введите своё местоположение (город):')
                return self.users_output()

            elif self.show_weather is True:
                if command.lower() != 'выход' and command.isdigit() is False:
                    return self.find_weather(update, command)
                else:
                    if command.isdigit() is True:
                        update.message.reply_text('Вы ввели число!'
                                                  '\nВведите запрос заново или введите <выход>')
                        return self.users_output(update)  # может появиться ошибка с двумя сообщениями

        if command.lower() == 'выход':
            if self.cards_game is False and self.show_weather is False:
                print('\nВыход')
                self.already_started = 0
                return self.stop(update, context)

            elif self.show_weather is True:
                print('\nВыход из погоды')
                update.message.reply_text('Вы вышли из просмотра погоды')
                self.show_weather = False
                return self.DEFINE
            else:
                print('\nВыход из карт')
                update.message.reply_text('\nВы уверены что хотите выйти?'
                                          '\nВаши 50 монет не сохранятся')
                self.sure = True
                return self.DEFINE

        elif self.cards_game is True and self.sure is True:
            if command.lower() == 'да':
                self.cards_game = False
                self.sure = False
                select_money = self.cur.execute('''SELECT money FROM money WHERE nik = ?''', (self.nik,)).fetchall()
                print(select_money)

                for i in select_money:
                    for j in i:
                        update_value = self.cur.execute('''UPDATE money SET money = ? WHERE nik = ?''',
                                                        (int(j) - 50, self.nik)).fetchall()
                        self.con.commit()

                update.message.reply_text('\nВы вышли из карт'
                                          '\nВведите <карты> или <монетка> для игры')
                self.koloda = self.koloda_forever
                self.player.clear()
                self.bot.clear()
                return self.DEFINE

            elif command.lower() == 'нет':
                update.message.reply_text('Вы не вышли из карт')
                self.sure = False

        if self.cards_game is True:
            if command.lower() == 'посмотреть карты':
                print('\nПросмотр карт')
                return self.show_cards(update, context)

            elif command.lower() == 'управление':
                print('\nУправление')
                return self.controls(update, context)

            elif command.lower() == 'сделать ход':
                print('\nХод игрока')
                return self.player_choose_card(update, context)

            elif command == 'INSTANT_WIN':
                print('\nADMIN: мгновенная победа')
                return self.pobeda('b', update, context)

            elif command.lower() == 'начать игру':
                return self.bot_move(update, context)

    def main(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.go)],
            states={
                self.DEFINE: [MessageHandler(Filters.text & ~Filters.command, self.defining_command)],
                self.DEFINE_CARD: [MessageHandler(Filters.text & ~Filters.command, self.define_card)],
                self.LOGIN_NIKNAME: [MessageHandler(Filters.text & ~Filters.command, self.login_password)],
                self.LOGIN_PASSWORD: [MessageHandler(Filters.text & ~Filters.command, self.login_password_one_more)],
                self.REGISTER: [MessageHandler(Filters.text & ~Filters.command, self.register)],
                self.START: [MessageHandler(Filters.text & ~Filters.command, self.go)],
                self.COIN: [MessageHandler(Filters.text & ~Filters.command, self.flip)],
                self.EXIT_DURING_MOVES: [MessageHandler(Filters.text & ~Filters.command, self.exit_during_moves)]
            },
            fallbacks=[CommandHandler('stop', self.stop), CommandHandler('controls', self.controls),
                       CommandHandler('show_cards', self.show_cards),
                       CommandHandler('player_choose_card', self.player_choose_card),
                       CommandHandler('player_choose_answer', self.player_choose_answer),
                       CommandHandler('bot_move', self.bot_move)]
        )
        self.dp.add_handler(conv_handler)

        updater.start_polling()

        # Ждём завершения приложения.
        # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
        updater.idle()


if __name__ == '__main__':
    game = Class_game()
    game.main()