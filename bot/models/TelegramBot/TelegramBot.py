import yaml
from telegram.ext import Updater


class TelegramBot:
    """
    TelegramBot class to interact with Telegram through Python

    To use, you have to configure it in config.yml file
    Follow the instructions in README to do this

    """

    def __init__(self):
        with open("config.yml", "r") as file:
            data = yaml.safe_load(file)
            self.user = data["user"]
            token = data["telegram_token"]
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def send_message(self, message):
        """
        Send a message to user

        """
        self.updater.bot.sendMessage(chat_id=self.user, text=message)

    def send_file(self, file):
        """
        Send a file to user

        """
        self.updater.bot.sendDocument(chat_id=self.user, document=file)
