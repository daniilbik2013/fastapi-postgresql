import telebot
import psycopg
import logging
from filesbot.database import OrderRepository
from dotenv import load_dotenv
import os
from filesbot.keyboards import main, main_menu, menu_back

logging.basicConfig(
level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

repo = OrderRepository()

token = os.getenv('TOKEN_TELEGRAM')
bot = telebot.TeleBot(token)
admin_id =int(os.getenv('TELEGRAM_ID'))
user_data = {}

@bot.message_handler(commands=['start'])
def start(m):
    status = repo.check_Register(m.from_user.id)
    is_admin = (m.chat.id == admin_id)
    caption = 'Bot for leads and sending applications taking them into account in your personal web account.You can order such a bot from @duovss'
    markup = main() if (is_admin or status == 1) else main_menu()
    try:
            with open('icons/horizontalweb.jpeg', 'rb') as photo:
                bot.send_photo(m.chat.id, photo=photo, caption=caption, reply_markup=markup)
    except FileNotFoundError:
            bot.send_message(m.chat.id, caption, reply_markup=markup)
 
@bot.callback_query_handler(func=lambda c: True)
def call(c):
	if c.data == 'what':
		bot.send_message(c.message.chat.id, 'This is a system for recording applications or leads with a personal web account for accounting.', reply_markup=main_menu())
	elif c.data == 'back':
		bot.delete_message(c.message.chat.id, c.message.message_id)
		status = repo.check_Register(c.message.from_user.id)
		is_admin = (c.message.chat.id == admin_id)
		text = 'Bot for leads and sending applications taking them into account in your personal web account.You can order such a bot from @duovss'
		markup = main() if (is_admin or status == 1) else main_menu()
		try:
		          	with open('icons/horizontalweb.jpeg', 'rb') as photo:
		          		bot.send_photo(c.message.chat.id, photo=photo, caption=text, reply_markup=markup)
		except FileNotFoundError:
			bot.send_message(c.message.chat.id, text, reply_markup=markup)
	elif c.data == 'send':
		chat_id = c.message.chat.id
		
		user_data[chat_id] = {}
		
		bot.answer_callback_query(c.id)
		msg = bot.send_message(chat_id, 'Lets fill out the form to submit an application.\n *Step 1 / 4.*\nSend your name in the chat Or click the "Back" button. Maximum length: 28 characters', reply_markup=menu_back(), parse_mode='Markdown')
		bot.register_next_step_handler(msg, process_name)
def process_name(m):
    chat_id = m.chat.id
    if len(m.text) > 28:
        msg = bot.send_message(chat_id, 'Max 28 chars. Try again:', reply_markup=menu_back())
        bot.register_next_step_handler(msg, process_name)
        return
    user_data[chat_id]['name'] = m.text
    msg = bot.send_message(chat_id, 'Step 2 / 4. Send your phone number:', reply_markup=menu_back())
    bot.register_next_step_handler(msg, process_phone)

def process_phone(m):
    chat_id = m.chat.id
    if len(m.text) > 20:
        msg = bot.send_message(chat_id, 'Max 20 chars. Try again:', reply_markup=menu_back())
        bot.register_next_step_handler(msg, process_phone)
        return
    user_data[chat_id]['phone'] = m.text
    msg = bot.send_message(chat_id, 'Step 3 / 4. Send the short name of the order:', reply_markup=menu_back())
    bot.register_next_step_handler(msg, process_title)

def process_title(m):
    chat_id = m.chat.id
    if len(m.text) > 100:
        msg = bot.send_message(chat_id, 'Max 100 chars. Try again:', reply_markup=menu_back())
        bot.register_next_step_handler(msg, process_title)
        return
    user_data[chat_id]['title'] = m.text
    msg = bot.send_message(chat_id, 'Step 4 / 4. Send a description: Max length: 420 chars', reply_markup=menu_back())
    bot.register_next_step_handler(msg, process_description)

def process_description(m):
    chat_id = m.chat.id
    if len(m.text) > 420:
        msg = bot.send_message(chat_id, 'Max 420 chars. Try again:', reply_markup=menu_back())
        bot.register_next_step_handler(msg, process_description)
        return
    user_data[chat_id]['description'] = m.text
    get_result(m)

def get_result(m):
    chat_id = m.chat.id
    data = user_data.get(chat_id)
    if not data:
        bot.send_message(chat_id, 'Error. Try again.', reply_markup=menu_back())
        return

    name = data.get('name')
    phone = data.get('phone')
    title = data.get('title')
    description = data.get('description')
    username = m.from_user.username or 'No username'
    success = repo.add_order(chat_id, name, username, phone, title, description)
    if success:
    	bot.send_message(chat_id, 'Request saved!', reply_markup=menu_back())
    	bot.send_message(admin_id, f'New request! Sender: @{username}')

    del user_data[chat_id]

if __name__ == '__main__':
	bot.infinity_polling()