import psycopg
from dotenv import load_dotenv
import logging
import os

# TODO: перевести бота на aiogram + asyncpg когда появится доступ к компу/серверу
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()
class OrderRepository:
	def __init__(self):
		self.dsn = os.getenv('DB_SETTING')
		self._init_db()
	def _init_db(self):
		try:
			with psycopg.connect(self.dsn) as conn:
				cur = conn.cursor()
				cur.execute("""
					CREATE TABLE IF NOT EXISTS user_orders(
					id SERIAL PRIMARY KEY,
         		   user_id BIGINT,
      		      name TEXT,
		            username TEXT,
		            number TEXT,
		            title TEXT,
		            description TEXT,
		            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		            status TEXT DEFAULT 'new'
				)""")
				cur.execute("""
					CREATE TABLE IF NOT EXISTS users(
					id SERIAL PRIMARY KEY,
					user_id BIGINT,
					is_Register INTEGER DEFAULT 0
				)""")
				conn.commit()
		except psycopg.OperationalError as e:
			logger.critical(f'Ошибка в подключении при создании базы данных: {e}')
		except Exception as e:
			logger.critical(f'Неизвестная ошибка в создании базы данных: {e}')
	
	def check_Register(self, user_id):
		try:
			with psycopg.connect(self.dsn) as conn:
				cur = conn.cursor()
				cur.execute("SELECT is_Register FROM users WHERE user_id = %s", (user_id,))
				row = cur.fetchone()
				return row[0] if row else None
		except psycopg.OperationalError as e:
			logger.critical(f'Ошибка в подключении при запросе статуса регистрации: {e}')
			return None
		except Exception as e:
			logger.critical(f'Неизвестная ошибка в запросе статуса регистрации: {e}')
			return None
	
	def add_order(self, user_id, name, username, number, title, description):
		try:
			with psycopg.connect(self.dsn) as conn:
				cur = conn.cursor()
				cur.execute("INSERT INTO user_orders(user_id, name, username, number, title, description) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, name, username, number, title, description))
				conn.commit()
				return True
		except psycopg.OperationalError as e:
			logger.critical(f'Ошибка в подключении при добавлении заявки: {e}')
			return False
		except Exception as e:
			logger.critical(f'Неизвестная ошибка в добавлении заявки: {e}')
			return False