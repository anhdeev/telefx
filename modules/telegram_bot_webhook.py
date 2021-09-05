from modules.common import enMarketPair, enTimeframe
from telegram import Update, Bot
import os, sys
from flask import Flask, request, render_template
import json
import logging
import subprocess
import queue
from urllib import parse

#sys.path.append(os.path.abspath(os.path.join('..')))

from modules.messager import Messager, MY_CHAT_ID

class TelegramWebhookBot(object):
    def __init__(self):
        self.key = os.getenv('TELEGRAM_KEY')
        self.host = os.getenv('HOST')
        self.bot = Bot(token=self.key)
        self.https_app = Flask(__name__, template_folder='../templates')
        self.cmd_queue = {}

        @self.https_app.route('/')
        def index():
            return render_template('upload_cert.html', host=self.host, botKey=self.key)

        @self.https_app.route('/webhook', methods=['POST'])
        def webhook_handler(self=self):
            try:
                logging.info("Method: %s" % request.method)
                if request.method == "POST":
                    # retrieve the message in JSON and then transform it to Telegram object
                    update = Update.de_json(request.get_json(force=True), self.bot)

                    messager = Messager(update)
                    parsedMsg = messager.parse_command()
                    if(not parsedMsg):
                        return 'ok'
                        
                    if parsedMsg["is_valid"]:
                        logging.debug("[webhook_handler] parsedMsg ", parsedMsg)
                        self.cmd_queue[parsedMsg["pair"]] = parsedMsg
                        response = parsedMsg["pair"][2:] + "-" + parsedMsg["frame"][9:] + " accepted."
                        self.bot.sendMessage(chat_id=parsedMsg["chat_id"], text=response)
                    else:
                        logging.error("[Error] Request message wrong format")
                        self.bot.sendMessage(chat_id=parsedMsg["chat_id"], text=parsedMsg["err_msg"])
                else:
                    logging.error("[Error] Request method=", request.method)
            except Exception as e: # work on python 3.x
                logging.error('[Exception][webhook_handler]: '+ str(e))
                self.bot.sendMessage(chat_id=MY_CHAT_ID, text="Error:" + str(e))

            return 'ok'

        @self.https_app.route("/getMessage", methods=['GET'])
        def get_msg(self=self):
            pair = request.args.get('pair')
            if(not pair):
                return 'none'
            msg = self.cmd_queue.get(pair)
            if(msg):
                self.cmd_queue[pair] = None
                return msg
            else:
                return 'none'

        @self.https_app.route("/sendMessage", methods=['POST'])
        def send_msg(self=self):
            body = request.json
            logging.info("[sendcmd] data: ", body)
            if not body:
                return 'none'

            chat_id = body.get("chat_id")
            if body["msgType"] == "photo":
                self.bot.send_photo(chat_id=chat_id, photo=open(body["photo_uri"], 'rb'))
            elif body["msgType"] == "txt":
                self.bot.sendMessage(chat_id=chat_id, text=body["message"])
            elif body["msgType"] == "object":
                self.bot.sendMessage(chat_id=chat_id, text=json.dumps(body))
            else:
                return 'none'
                
            return 'ok'

    def send_message(self, chat_id, result):
        self.bot.sendMessage(chat_id=chat_id, text=result)

    def run(self):
        logging.info("Please access https:<domain>/ to register webhook portal for udpates!")
        self.https_app.run(host='0.0.0.0', port='443', ssl_context=('ssl/public.pem', 'ssl/private.key'))
        #self.https_app.run(host='10.148.0.7', port='80')
