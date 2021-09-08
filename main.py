#!/usr/bin/env python
import os
import json
import logging
import threading
from modules.telegram_bot_webhook import TelegramWebhookBot
from grafana import grafana

logging.getLogger().setLevel(logging.INFO)
bot = TelegramWebhookBot()

def run_bot():
    global bot
    bot.run()

if __name__ == "__main__":
    print(os.getenv("FLASK_ENV"))
    
    graph = threading.Thread(target=grafana.run, args=())
    graph.start()

    run_bot()
