import asyncpg
import logging

logging.basicConfig(
level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s',)
logger = logging.getLogger(__name__)

class Order:
	def __init__(self, id, user_id, name, username, number, title, description, created_at, status='new'):
		self.id = id
		self.user_id = user_id
		self.name = name
		self.username = username
		self.number = number
		self.title = title
		self.description = description
		self.created_at = created_at
		self.status = status

class OrderRepository:
	def __init__(self, pool):
		self.pool = pool
	
	async def get_all(self):
		try:
		    rows = await self.pool.fetch("SELECT * FROM user_orders")
		    return [Order(*row) for row in rows]
		except (asyncpg.ConnectionDoesNotExistError, OSError) as e:
		    logger.critical(f"Пропало соединение с базой: {e}")
		    return []
		except Exception as e:
		    logger.critical(f"Ошибка в базе данных на моменте запроса данных: {e}")
		    return []
	
	async def get_by_id(self, order_id):
		try:
		    row = await self.pool.fetchrow("SELECT * FROM user_orders WHERE id = $1", order_id)
		    if row:
		        return Order(*row)
		    return None
		except (asyncpg.ConnectionDoesNotExistError, OSError) as e:
		    logger.critical(f"Пропало соединение с базой при запросе данных по айди: {e}")
		    return None
		except Exception as e:
		    logger.critical(f"Ошибка в базе данных при запросе данных по айди: {e}")
		    return None
	
	async def get_all_limit(self, limit):
		try:
		    rows = await self.pool.fetch("SELECT * FROM user_orders ORDER BY id DESC LIMIT $1", limit)
		    return [Order(*row) for row in rows]
		except (asyncpg.ConnectionDoesNotExistError, OSError) as e:
		    logger.critical(f"Пропало соединение с базой при запросе данных с лимитом: {e}")
		    return []
		except Exception as e:
		    logger.critical(f"Ошибка в базе данных при запросе данных с лимитом: {e}")
		    return []

	async def delete(self, order_id):
		try:
		    async with self.pool.acquire() as conn:
		    	await conn.execute("DELETE FROM user_orders WHERE id = $1", order_id)
		    	logger.info(f"Успешное удаление заявки #{order_id}")
		    	return True
		except (asyncpg.ConnectionDoesNotExistError, OSError) as e:
		    logger.critical(f"Пропало соединение с базой при удалении заказа #{order_id}: {e}")
		    return False
		except Exception as e:
		    logger.critical(f"Ошибка в базе данных при удалении заказа #{order_id}: {e}")
		    return False

	async def update_status(self, order_id, new_status):
		try:
		    async with self.pool.acquire() as conn:
		    	await conn.execute("UPDATE user_orders SET status = $1 WHERE id = $2", new_status, order_id)
		    	logger.info(f"Успешное обновление заказа #{order_id}")
		    	return True
		except (asyncpg.ConnectionDoesNotExistError, OSError) as e:
		    logger.critical(f"Пропало соединение с базой при редактировании статуса заказа #{order_id} на {new_status}: {e}")
		    return False
		except Exception as e:
		    logger.critical(f"Ошибка в базе данных при редактировании статуса заказа #{order_id}: {e}")
		    return False