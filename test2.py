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
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Option 1", callback_data="option_1"))
    markup.add(InlineKeyboardButton("Option 2", callback_data="option_2"))
    await bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup)

# Handle button presses
@bot.callback_query_handler(func=lambda call: True)
async def handle_callback_query(call):
    if call.data == "option_1":
        await bot.answer_callback_query(call.id, "You selected Option 1!")
        await bot.send_message(call.message.chat.id, "You chose Option 1.")
    elif call.data == "option_2":
        await bot.answer_callback_query(call.id, "You selected Option 2!")
        await bot.send_message(call.message.chat.id, "You chose Option 2.")
    else:
        await bot.answer_callback_query(call.id, "Unknown option!")

# Start polling
import asyncio
async def main():
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())
