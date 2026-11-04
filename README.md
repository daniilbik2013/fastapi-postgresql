# Telegram CRM

A lead management system consisting of a Telegram bot (for clients) and a web dashboard (for administrators).

## Tech Stack

- Backend: Python 3.13, FastAPI, Telebot.
- Database: PostgreSQL (Neon cloud hosting).
- Database Driver: psycopg 3.
- Frontend: HTML, CSS, Vanilla JS (Fetch API).
- Security: slowapi (Rate Limiting).

## Features

- Step-by-step form in the Telegram bot (name, phone, description).
- Saving leads to a cloud database.
- Web dashboard with a list of leads (limits, pagination).
- Updating lead status (In progress, Done).
- Deleting a lead.
- Rate Limiting (DDoS and spam protection).

## Installation and Setup

1. Clone the repository:
   git clone https://github.com/YOUR_USERNAME/telegram-crm.git
   cd telegram-crm

2. Install dependencies:
   pip install -r requirements.txt

3. Create a .env file in the project root and add the following variables:
   TOKEN_TELEGRAM=your_token
   TELEGRAM_ID=your_id
   DB_SETTING=postgresql://user:pass@host/db

4. Run the bot:
   python bot.py

5. Run the web server:
   python app.py

## License
MIT