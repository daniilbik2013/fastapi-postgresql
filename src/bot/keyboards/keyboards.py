from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def main():
    keyboard = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('Open web account', url='http://127.0.0.1:8000/')
    button_2 = InlineKeyboardButton('Send a request', callback_data='send')
    keyboard.add(button_1)
    keyboard.add(button_2)
    return keyboard
def main_menu():
    keyboard = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton('What is this ?', callback_data='what')
    button_2 = InlineKeyboardButton('Send a request', callback_data='send')
    keyboard.add(button_1)
    keyboard.add(button_2)
    return keyboard
def menu_back():
    keyboard = InlineKeyboardMarkup()
    button_back = InlineKeyboardButton('Back', callback_data='back')
    keyboard.add(button_back)
    return keyboard