from colorama import init, Fore
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
import random
import math
from time import sleep
import sys

init()
running = True
cards_n = 36
cards = ['PIK', 'TRE', 'CHER', 'BUB']
vel_card = {'Шесть': 1, 'Семь': 2, 'Восемь': 3, 'Девять': 4, 'Десять': 5, 'Валет': 6, 'Дама': 7, 'Король': 8, 'Туз': 9}
n_player_cards = 6
n_bot_cards = 6
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

player = list()
bot = list()
first_turn = ''
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


class Game:
    def controls(self):
        print('\nУправление')
        update.message.reply_text('Управление\n'
                                  '1 - посмотреть свои карты\n'
                                  '2 - сделать ход\n'
                                  '3 - управление\n'
                                  '4 - выход')
        return 1

    def show_cards(self):
        print('\nПоказ карт')
        for i in player:
            return f'{player.index(i) + 1}: {i}'

    def giving_cards(self, n):
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

        print('КОЗЫРЬ:', cozir)
        print('ВАШИ КАРТЫ:')
        self.show_cards()
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

    def exit(self):
        global running
        running = False
        return running

    def player_move(self):
        global n_bot_cards, n_player_cards, cozir_flag
        move = True
        print('\nВыберите карту: ')
        self.show_cards()
        answ = ''

        while move:
            try:
                card = int(input())
            except ValueError:
                print('Введите число')
                self.player_move()
            try:
                print(player[card - 1])
                answ = player[card - 1]
                n_player_cards -= 1
                if n_player_cards == 0:
                    print('ВЫ ВЫИГРАЛИ')
                    self.pobeda('p')
                del player[player.index(player[card - 1])]
                if n_player_cards < 6:
                    if len(koloda) != 0:
                        card = random.choice(koloda)
                        player.append(card)
                        del koloda[koloda.index(card)]
                        n_player_cards += 1
                    elif cozir_flag:
                        player.append(cozir)
                        cozir_flag = False
                        n_player_cards += 1
                self.bot_answ(answ)
                print('Теперь ходит бот')
                self.bot_move()
                move = False
            except IndexError:
                print('Числа нет в списке')
        return answ

    def player_answer(self, bot_hod):
        global player, n_player_cards, n_bot_cards, cozir, coz, cozir_flag
        Flag = False
        print('Чем ответим?')
        self.show_cards()
        print('Напишите <взять>, если хотите взять')
        move = True
        while move:
            try:
                card = input()
                if card.lower() != 'взять':
                    card = int(card)
                    if player[card - 1].split('_')[1] != cozir.split('_')[1]:
                        if bot_hod.split('_')[1] == player[card - 1].split('_')[1]:
                            if vel_card[player[card - 1].split('_')[0]] > vel_card[bot_hod.split('_')[0]]:
                                player_answ = player[card - 1]
                                Flag = True
                            else:
                                print('Выбранная вами карта не побивает ' + bot_hod)
                        else:
                            print('Выбранная вами карта не побивает ' + bot_hod)
                    elif bot_hod.split('_')[1] != cozir.split('_')[1]:
                        Flag = True
                        player_answ = player[card - 1]
                    else:
                        if vel_card[player[card - 1].split('_')[0]] > vel_card[bot_hod.split('_')[0]]:
                            player_answ = player[card - 1]
                            Flag = True
                        else:
                            print('Выбранная вами карта не побивает ' + bot_hod)
                else:
                    print('Вы берете:' + bot_hod)
                    player.append(bot_hod)
                    n_player_cards += 1
                    self.bot_move()
            except ValueError:
                print('Что-то пошло не по плану, возможно вы написали неверное число')
            if Flag:
                print('Вы побили ' + bot_hod + ' картой ' + player_answ)
                del player[card - 1]
                n_player_cards -= 1
                if n_player_cards == 0:
                    print('ВЫ ВЫИГРАЛИ')
                    self.pobeda('p')
                if n_player_cards < 6:
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
                print('Теперь ваш ход, удачи')
                self.player_move()

    def bot_move(self):
        global bot, cards_n, cozir, n_bot_cards, n_player_cards, cozir_flag
        spisok_card = {'Шесть': [], 'Семь': [], 'Восемь': [], 'Девять': [], 'Десять': [], 'Валет': [], 'Дама': [],
                       'Король': [], 'Туз': []}
        answ = []
        print(koloda)
        print(bot)
        print(len(koloda))
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
        print('Бот атакует: ' + answ[0])
        del bot[bot.index(answ[0])]
        n_bot_cards -= 1
        if n_bot_cards == 0:
            print('БОТ ВЫИГРАЛ')
            pobeda('b')
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
        self.player_answer(answ[0])

    def bot_answ(self, movek):
        global bot, vel_card, cozir, n_player_cards, n_bot_cards, cozir_flag
        answ = ''
        print(bot)
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
            print(answ)
            del bot[bot.index(answ)]
            n_bot_cards -= 1
            if n_bot_cards == 0:
                print('БОТ ВЫИГРАЛ')
                self.pobeda('b')
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
                print('Бот не может отбиться, бот принимает')
                bot.append(movek)
                n_bot_cards += 1
                self.player_move()
            else:
                print('Бот бьет ' + movek + ' картой ' + answ)
                del bot[bot.index(answ)]
                n_bot_cards -= 1
                if n_bot_cards == 0:
                    print('БОТ ВЫИГРАЛ')
                    self.pobeda('b')
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

    def menu(self):
        global running
        update.message.reply_text(
            'Приветствуем в картах! Если хотите выйти - введите EXIT. Для начала игры введите PLAY.\n'
            'Вы можете выйти из игры в любое время.')

        already_started = 0

        while running:
            start = input()  # играть или выйти

            if start == 'EXIT':
                self.exit()

            elif start == 'PLAY':
                if already_started == 0:
                    already_started = 1
                    self.game()
                else:
                    update.message.reply_text('Игра уже начата!')
            else:
                update.message.reply_text('Введите EXIT или PLAY')

    def game(self):
        global first_turn
        self.giving_cards(6)
        if first_turn == 'player':
            self.controls()
        elif first_turn == 'bot':
            sleep(2)
            self.bot_move()

        while running:
            choose = input()

            if choose == '1':
                print('Ваша колода:')
                self.show_cards()
            if choose == '2':
                self.player_move()
            if choose == '3':
                self.controls()
            if choose == '4':
                self.exit()

    def pobeda(self, who_wins):
        if who_wins == 'p':
            print('МОЛОДЕЦ')
            sys.exit()
        if who_wins == 'b':
            print('НЕ ПОВЕЗЛО? ПОПРОБУЙ ЕЩЕ РАЗ')
            sys.exit()


game = Game()


def stop(update, context):
    return ConversationHandler.END


def controls(update, context):
    update.message.reply_text('Управление\n'
                              '1 - посмотреть свои карты\n'
                              '2 - сделать ход\n'
                              '3 - управление\n'
                              '4 - выход')
    word = update.message.text
    return 1


def show_cards(update, context):
    update.message.reply_text(game.show_cards())


def second(update, context):
    update.message.reply_text('Второй вопрос')
    return ConversationHandler.END


def first(update, context):
    update.message.reply_text('Первый вопрос')
    return 2


def main():
    updater = Updater('5102501109:AAEq0uyJj_Gy4pb3QbyHQMjzU7ayV26Q7iE', use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', controls)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, first)],
            2: [MessageHandler(Filters.text & ~Filters.command, second)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
