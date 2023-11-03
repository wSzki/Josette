import os

import telebot
import yt_dlp

from utils import get_daily_horoscope

BOT_TOKEN = "6828287802:AAEMo3QZsWPTwQ8FcfUlCGtaPXQD3x5tOdA"

bot = telebot.TeleBot(BOT_TOKEN)

        "yt-dlp",
        "--extract-audio",
        "--audio-format", "aac",
        "--add-metadata",
        "--embed-thumbnail",
        "--batch-file", "/playlist/playlist.txt",
        "--download-archive", "/archive/archive.txt",
        "-o", "/music/%(title)s.%(ext)s"
        ]



def download_video(url, message):
    try:
        ydl.download([url])
        return 0
    except Exception as e:
        bot.reply_to(message, "❌ Error")
        return 1

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    os.system('echo "hello" >> /app/bot.log')
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['bisou'])
def send_welcome(message):
    bot.reply_to(message, "Je t'aime tant bisou - signé José")


@bot.message_handler(commands=['get'])
def upload(message):
    bot.reply_to(message, "💿 Searching...")
    argument = message.text.split('/get')[-1]
    if (download_video(argument, message) == 0):
        bot.reply_to(message, "✅ Done")

# @bot.message_handler(commands=['horoscope'])
# def sign_handler(message):
    # text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    # sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    # bot.register_next_step_handler(sent_msg, day_handler)


# def day_handler(message):
    # sign = message.text
    # text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    # sent_msg = bot.send_message(
        # message.chat.id, text, parse_mode="Markdown")
    # bot.register_next_step_handler(
        # sent_msg, fetch_horoscope, sign.capitalize())


# def fetch_horoscope(message, sign):
    # day = message.text
    # horoscope = get_daily_horoscope(sign, day)
    # data = horoscope["data"]
    # horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    # bot.send_message(message.chat.id, "Here's your horoscope!")
    # bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()

