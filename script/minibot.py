# ==============================================================================
# ---------------------------------- IMPORTS -----------------------------------
# ==============================================================================

import os
import telebot
import sys
import subprocess



BOT_TOKEN = "6828287802:AAEMo3QZsWPTwQ8FcfUlCGtaPXQD3x5tOdA"
bot = telebot.TeleBot(BOT_TOKEN)

# ==============================================================================
# ----------------------------------- UPDATE -----------------------------------
# ==============================================================================

@bot.message_handler(commands=['bisou'])
def upload(message):
    bot.send_message(message.chat.id, "Bisou")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Salut")



bot.infinity_polling()


