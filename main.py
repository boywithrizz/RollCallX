import telebot

# Replace with your actual token
bot = telebot.TeleBot("7551528861:AAEpxbtxw9cOhBbE0-ldqU2u8RowHflK9ZE")
click = 0 

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id
    text = message.text
    click+=1

    response = f"Hello {first_name} {last_name},\nWelcome to the LPowerBot\n It is your message number : {click}!"
    bot.reply_to(message, response)

bot.polling()