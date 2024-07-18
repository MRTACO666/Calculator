import telebot
from telebot import types

# Replace with your actual token
BOT_TOKEN = '7222964727:AAECsNxSUqgEp6moqtCmJb-3HmkjILpKAOs'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
  """Starts the calculator."""
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(
      types.KeyboardButton('+'),
      types.KeyboardButton('-'),
      types.KeyboardButton('*'),
      types.KeyboardButton('/'),
      types.KeyboardButton('='),
  )
  bot.send_message(message.chat.id, 'Введи действие', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['+', '-', '*', '/'])
def operation(message):
  """Handles the chosen operation."""
  global operator, first_number
  operator = message.text
  bot.send_message(message.chat.id, 'Первое число:')
  bot.register_next_step_handler(message, get_first_number)

@bot.message_handler(func=lambda message: message.text.isdigit())
def get_first_number(message):
  """Gets the first number."""
  global first_number
  first_number = int(message.text)
  bot.send_message(message.chat.id, 'Второе число:')
  bot.register_next_step_handler(message, get_second_number)

@bot.message_handler(func=lambda message: message.text.isdigit())
def get_second_number(message):
  """Gets the second number."""
  global second_number
  second_number = int(message.text)
  bot.send_message(message.chat.id, 'Ещё раз введите действие:')
  bot.register_next_step_handler(message, calculate)

@bot.message_handler(func=lambda message: message.text == '=')
def calculate(message):
  """Calculates the result."""
  global result

  if operator == '+':
    result = first_number + second_number
  elif operator == '-':
    result = first_number - second_number
  elif operator == '*':
    result = first_number * second_number
  elif operator == '/':
    if second_number == 0:
      bot.send_message(message.chat.id, 'Даун делить на ноль нельзя.')
      return
    else:
      result = first_number / second_number

  bot.send_message(message.chat.id, f'Ответ: {result}')

bot.polling(non_stop=True)