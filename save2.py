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

# ВСЕ НОВЫЕ КОМАНДЫ ЗАСОВЫВАТЬ В FALLBACKS!!!
# Через них возвращать DEFINE, из-за чего процесс распознавания команд будет непрерывным и игра не завершится!

dp = updater.dispatcher

init()
running = True
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

DEFINE, DEFINE_CARD, DEFINE_PLAYER_ANSWER = range(3)

player = list()
bot = list()
first_turn = 'player'
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
            pobeda('p')
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
                pobeda('p')

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
            update.message.reply_text('Бот не может отбиться, бот принимает')
            return bot_taking_cards(movek, update, context)   # здесь начинается ошибка
        else:
            update.message.reply_text('Бот бьет ' + movek + ' картой ' + answ)
            del bot[bot.index(answ)]
            n_bot_cards -= 1

            if n_bot_cards == 0:
                update.message.reply_text('Бот победил!')
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


def game(update, context):
    global first_turn
    giving_cards(6, update, context)
    if first_turn == 'player':
        controls(update, context)
    elif first_turn == 'bot':
        print('Бот ходит')
#        sleep(2)
#        bot_move(update)


def pobeda(who_wins):
    if who_wins == 'p':
        print('МОЛОДЕЦ')
        return ConversationHandler.END
    if who_wins == 'b':
        print('НЕ ПОВЕЗЛО? ПОПРОБУЙ ЕЩЕ РАЗ')
        return ConversationHandler.END


def stop(update, context):
    return ConversationHandler.END


def controls(update, context):
    reply_keyboard = [['Посмотреть карты', 'Сделать ход'],
                      ['Управление', 'Выход']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text('Что вы хотите сделать?',
                              reply_markup=markup)

    return DEFINE


def start(update, context):
    global already_started
    if already_started == 0:
        update.message.reply_text('Добро пожаловать в игру, хотите продолжить?\n'
                                  'Да/Нет')
        already_started = 1
        return DEFINE
    else:
        update.message.reply_text('Игра уже началась! Введите /stop если хотите закончить\n'
                                  'и начать заново')


def define_card(update, context):
    global card, answering, n_player_cards, player
    card = update.message.text      # получаем сообщение из player_choose_card

    if answering == 'player' and card == 'взять':
        print(f'Игрок берёт карту: {bot_answer_answer}')
        update.message.reply_text(f'Вы берёте карту {bot_answer_answer}')
        player.append(bot_answer_answer)
        n_player_cards += 1
        bot_move(update, context)
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


def defining_command(update, context):
    global already_started
    command = update.message.text

    if command == 'Да':
        print('\nНачало игры')
        return game(update, context)

    elif command == 'Нет':
        print('\nВыход до начала игры')
        return ConversationHandler.END

    elif command == 'Посмотреть карты':
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
        entry_points=[CommandHandler('start', start)],
        states={
            DEFINE: [MessageHandler(Filters.text & ~Filters.command, defining_command)],
            DEFINE_CARD: [MessageHandler(Filters.text & ~Filters.command, define_card)],
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


@bot.message_handler(commands=['start'])
def location(message):
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('Локация', request_location=True)
    markup.row(button)

    bot.send_message(message.chat.id, 'Ananas', reply_markup=markup)


bot.polling()

return DEFINE
if message != 'Выход':
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": message,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        return find_weather(update, context, message)
    else:
        update.message.reply_text('Вы ввели что-то неверно.'
                                  '\nВведите заново или <выход> для выхода.')
else:
    update.message.reply_text('Вы вышли из просмотра погоды')
    return DEFINE