```python
import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter, DeclensionByCases

bot = telebot.TeleBot(TOKEN)

# Greeting
@bot.message_handler(commands=['start'])
def start(message):
    text = f"Welcome, {message.from_user.first_name}!\n\nI am the Currency Converter, and I can:" \
           f"\n- convert your currency using the command <currency name> <target currency> " \
           f"<amount of currency to convert> (separated by spaces)." \
           f"\nFor example: ruble euro 1\n" \
           f"\n- show the currencies you can convert using the command \n/values;" \
           f"\n- remind you what I can do using the command \n/help."
    bot.send_message(message.chat.id, text)

# Handling the help command:
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'To convert currency, write me a command like this:' \
           '\n<currency name> <target currency> <amount of currency to convert> separated by spaces.' \
           '\nFor example: ruble euro 1\n' \
           '\nTo see the currencies I can convert, enter the command \n/values'
    bot.reply_to(message, text)

# List of currencies for conversion
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'I can convert:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# Catching Exception
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('\nThe number of parameters does not match!\n'
                               '\nPlease write like this:\n<currency name> ' \
                               '<target currency> <amount of currency to convert> separated by spaces'
                               '\nOtherwise, I do not understand you :(')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Oops, you wrote something wrong:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Something went wrong :(\n\n{e}\n'
                              f'\nBut it\'s not your fault, it\'s just one of those days.')
    else:
        inclined_quote = DeclensionByCases(quote, float(amount))
        inclined_base = DeclensionByCases(base, float(total_base))
        quote = inclined_quote.incline()
        base = inclined_base.incline()
        text = f'{amount} {quote} = {round(total_base, 5)} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()
