# Telegram CRM

A lead management system consisting of a Telegram bot (for clients) and a web dashboard (for administrators).

## Tech Stack

* Backend: Python 3.13 ![Python](https://img.shields.io/badge/Python-3.13-blue), FastAPI ![FastAPI](https://img.shields.io/badge/FastAPI-0.99-green), Telebot ![Telebot](https://img.shields.io/badge/Telebot-4.0-blue).
* Database: PostgreSQL ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue) (Neon cloud hosting).
* Database Driver: asyncpg, psycopg 3.
* Frontend: HTML, CSS, Vanilla JS (Fetch API).
* Security: slowapi (Rate Limiting).

## Features

* Step-by-step form in the Telegram bot (name, phone, description).
* Saving leads to a cloud database.
* Web dashboard with a list of leads (limits, pagination).
* Updating lead status (In progress, Done).
* Deleting a lead.
* Rate Limiting (DDoS and spam protection).

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/daniilbik2013/fastapi-postgresql.git
   cd fastapi-postgresql

2. Run the bot (from the project root):
   ```bash
   python -m src.bot.bot

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Create a .env file in the project root and add the following variables:
    ```env
    TOKEN_TELEGRAM=your_token
    TELEGRAM_ID=your_id
    DB_SETTING=postgresql://user:pass@host/db

5. Run the web server (from the project root):
    ```bash
    uvicorn src.app.app:app --reload