import telebot

import handler
import api

import config

bot = telebot.TeleBot(config.token,)
hh_api = api.hh_api(base_url = config.hh_url, service_token = config.hh_token)
imgbb_api = api.imgbb_api(config.imgbb_token)

handler = handler.Handler(bot, hh_api, imgbb_api)

@bot.message_handler()
def handle(message):
    handler.handle(message)

print("Bot started")
bot.infinity_polling()