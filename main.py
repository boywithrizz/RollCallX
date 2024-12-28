from telebot.async_telebot import AsyncTeleBot
import asyncio
# Replace with your bot token
TOKEN = '7551528861:AAEpxbtxw9cOhBbE0-ldqU2u8RowHflK9ZE'
bot = AsyncTeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
async def info(message):
    user = message.from_user
    await bot.reply_to(message,f'Hello {user.first_name} {user.last_name},\nThis bot is made by Ayush Yadav\nThis bot will give you a reward when you type send some message to it, Try it!')
@bot.message_handler(func=lambda message : True)
async def prank(message):
    with open("life-me.mp4","rb") as video:
        await bot.send_animation(message.chat.id,video,caption='Padhle jaakr saale!')

# Start polling
asyncio.run(bot.polling())