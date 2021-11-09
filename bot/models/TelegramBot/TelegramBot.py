import yaml
from telegram.ext import Updater


class TelegramBot:

    def __init__(self):
        with open("config.yml", "r") as file:
            data = yaml.safe_load(file)
            self.user = data["user"]
            token = data["telegram_token"]
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def send_message(self, message):
        self.updater.bot.sendMessage(chat_id=self.user, text=message)