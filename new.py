from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize the bot
bot = AsyncTeleBot(API_TOKEN)

# Command to send inline buttons
@bot.message_handler(commands=['start', 'menu'])
async def send_menu(message):
    await bot.reply_to(message,f'Hello {message.from_user.first_name} {message.from_user.last_name}')
# Start polling
import asyncio
async def main():
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())
