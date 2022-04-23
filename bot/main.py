import telebot

import handler
import api

import config

bot = telebot.TeleBot(config.token,)
api = api.hh_api(config.base_url, config.service_token)
handler = handler.Handler(bot, api)

@bot.message_handler()
def handle(message):
    handler.handle(message)

print("Bot started")
bot.infinity_polling()