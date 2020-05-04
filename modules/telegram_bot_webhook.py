import telegram
import os, sys
from flask import Flask, request, render_template
import json
import logging
import subprocess
import queue

#sys.path.append(os.path.abspath(os.path.join('..')))

from modules.messager import Messager

#TODO Store key in database
MY_TELEGRAM_KEY="1102340901:AAGV-PBEyXwfLeAgDkkJvQpI6mD4OGWStXM"

class TelegramWebhookBot(object):
    def __init__(self):
        self.key = MY_TELEGRAM_KEY
        self.bot = telegram.Bot(token=self.key)
        self.https_app = Flask(__name__, template_folder='../templates')
        self.cmd_queue = queue.Queue(maxsize=20)

        @self.https_app.route("/getcmd", methods=['GET'])
        def get_cmd():
            return self.cmd_queue.get()

        @self.https_app.route("/sendcmd", methods=['POST'])
        def send_cmd():
            cmd = request.get_data()
            self.bot.sendMessage(chat_id=MY_CHAT_ID, text=cmd)
            return "ok"

        @self.https_app.route('/')
        def index(): #TODO fix issue of register by template
            logging.info('Registered webhok succesfully')
            return render_template('upload_cert.html')

        @self.https_app.route('/webhook', methods=['POST'])
        def webhook_handler(self=self):
            logging.info("Method: %s" % request.method)
            if request.method == "POST":
                # retrieve the message in JSON and then transform it to Telegram object
                update = telegram.Update.de_json(request.get_json(force=True), self.bot)

                messager = Messager(update)
                chat_id, result = messager.execute_command()

            if chat_id:
                #self.bot.sendMessage(chat_id=chat_id, text=str(result))
                self.cmd_queue.push(str(result) + "@" + chat_id)
            else:
                pass

            return 'ok'

    def parse_message(self):
        # extract and filter information 
        pass

    def send_message(self, chat_id, result):
        self.bot.sendMessage(chat_id=chat_id, text=result)

    def run(self):
        logging.info("Please access https:<domain>/ to register webhook portal for udpates!")
        self.https_app.run(host='0.0.0.0', port='443', ssl_context=('ssl/public.pem', 'ssl/private.key'))
        #self.https_app.run(host='10.148.0.7', port='80')
