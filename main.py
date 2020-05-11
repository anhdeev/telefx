#!/usr/bin/env python
import os
import json
import logging
import threading
from modules.telegram_bot_webhook import TelegramWebhookBot

logging.getLogger().setLevel(logging.DEBUG)
bot = TelegramWebhookBot()

def run_bot():
    global bot
    bot.run()

if __name__ == "__main__":
    run_bot()