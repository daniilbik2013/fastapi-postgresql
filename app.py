from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel
from contextlib import asynccontextmanager
from database import OrderRepository
from dotenv import load_dotenv
import asyncpg
import os
import uvicorn

db_pool = None
repo = None
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
	global db_pool, repo
	db_pool = await asyncpg.create_pool(
	dsn = os.getenv('DB_SETTING'),
	min_size=2,
	max_size=10,
	command_timeout=30,
	max_inactive_connection_lifetime=300
	)
	repo = OrderRepository(db_pool)
	yield
	await db_pool.close()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/icons", StaticFiles(directory="icons"), name="icons")

class OrderCreate(BaseModel):
	user_id: int
	name: str
	username: str
	number: str
	title: str
	description: str
class UpdateStatus(BaseModel):
	status: str

@app.get('/')
async def index_page():
    return FileResponse("templates/index.html")

@app.get('/ui/orders')
async def orders_page():
    return FileResponse("templates/order.html")

@app.get('/ui/order/{order_id}')
async def order_page(order_id: int):
    return FileResponse("templates/settingOrders.html")

@app.get('/orders')
@limiter.limit("60/minute")
async def orders(request: Request):
	return await repo.get_all()

@app.get('/api/last-orders')
async def web_main():
	return await repo.get_all_limit(2)

@app.delete('/delete_order/{order_id}')
@limiter.limit("4/minute")
async def func_delete(request: Request, order_id):
	success = await repo.delete(order_id)
	return {'success': success}

@app.get('/orders/{order_id}')
@limiter.limit("60/minute")
async def setting_func(request: Request, order_id):
	order = await repo.get_by_id(order_id)
	if not order:
		raise HTTPException(status_code=404, detail='Данного заказа не существует')
	return order

@app.get('/order/limit/{limit}')
@limiter.limit("60/minute")
async def order_limit(request: Request, limit):
	if limit not in [5, 10, 20, 45]:
		raise HTTPException(status_code=404, detail='Невозможный лимит')
	return await repo.get_all_limit(limit)

@app.patch('/update_order/{order_id}')
@limiter.limit("10/minute")
async def update(request: Request, order_id: int, data: UpdateStatus):
	if not data:
		raise HTTPException(status_code=404, detail='Данных нету')
	success = await repo.update_status(order_id, data.status)
	return {'success': success}
if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)