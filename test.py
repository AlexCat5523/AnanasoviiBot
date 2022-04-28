from colorama import init, Fore
from telegram.ext import Updater, MessageHandler, Filters, ExtBot
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import CallbackQuery
import random
import math
from time import sleep
import sys

updater = Updater('5102501109:AAEq0uyJj_Gy4pb3QbyHQMjzU7ayV26Q7iE', use_context=True)

# Получаем из него диспетчер сообщений.
dp = updater.dispatcher

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


def controls(update, context):
    print('\nУправление')
    reply_keyboard = [['Посмотреть карты', 'Сделать ход'],
                      ['Управление', 'Выход']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Что вы хотите сделать?',
                              reply_markup=markup)


def defining_command(update):
    command = CallbackQuery.message
    print(command)
    if command == 'Посмотреть карты':
        show_cards(update)
    elif command == 'Сделать ход':
        player_move(update)
    elif command == 'Управление':
        controls(update, context)
    elif command == 'Выход':
        sys.exit()


def show_cards(update):
    global cozir
    print('\nПоказ карт')
    s = ''
    s += f'Козырь: {cozir}\n'
    s += f'Ваши карты: \n'
    for i in player:
        s += f'{player.index(i) + 1}: {i}\n'
    update.message.reply_text(s)


def giving_cards(n, update):
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

    show_cards(update)
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


def exit():
    global running
    running = False
    return running


def player_move(update):
    global n_bot_cards, n_player_cards, cozir_flag
    move = True
    print('\nВыберите карту: ')
    show_cards(update)
    answ = ''

    while move:
        try:
            card = int(input())
        except ValueError:
            print('Введите число')
            player_move(update)
        try:
            print(player[card - 1])
            answ = player[card - 1]
            n_player_cards -= 1
            if n_player_cards == 0:
                print('ВЫ ВЫИГРАЛИ')
                pobeda('p')
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
            bot_answ(answ)
            print('Теперь ходит бот')
            bot_move()
            move = False
        except IndexError:
            print('Числа нет в списке')
    return answ


def player_answer(bot_hod, update):
    global player, n_player_cards, n_bot_cards, cozir, coz, cozir_flag
    Flag = False
    print('Чем ответим?')
    show_cards(update)
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
                bot_move()
        except ValueError:
            print('Что-то пошло не по плану, возможно вы написали неверное число')
        if Flag:
            print('Вы побили ' + bot_hod + ' картой ' + player_answ)
            del player[card - 1]
            n_player_cards -= 1
            if n_player_cards == 0:
                print('ВЫ ВЫИГРАЛИ')
                pobeda('p')
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
            player_move(update)


def bot_move(update):
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
    player_answer(answ[0], update)


def bot_answ(movek):
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
            player_move()
        else:
            print('Бот бьет ' + movek + ' картой ' + answ)
            del bot[bot.index(answ)]
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


def start(update, context):
    game(update, context)


def game(update, context):
    global first_turn
    giving_cards(6, update)
    if first_turn == 'player':
        controls(update, context)
    elif first_turn == 'bot':
        sleep(2)
        bot_move(update)

    while running:
        print(update.message.text)
        choose = input()

        if choose == '1':
            print('Ваша колода:')
            show_cards(update)
        if choose == '2':
            player_move(update)
        if choose == '3':
            controls(update, context)
        if choose == '4':
            exit()


def pobeda(who_wins):
    if who_wins == 'p':
        print('МОЛОДЕЦ')
        sys.exit()
    if who_wins == 'b':
        print('НЕ ПОВЕЗЛО? ПОПРОБУЙ ЕЩЕ РАЗ')
        sys.exit()


def stop(update, context):
    return ConversationHandler.END


def second(update, context):
    update.message.reply_text('Второй вопрос')
    return ConversationHandler.END


def first(update, context):
    update.message.reply_text('Первый вопрос')
    return 2


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('ananas', start)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, first)],
            2: [MessageHandler(Filters.text & ~Filters.command, second)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()

    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
