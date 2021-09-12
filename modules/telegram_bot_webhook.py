from modules.common import enMarketPair, enTimeframe
from telegram import Update, Bot
import os, sys
from flask import Flask, request, render_template, Response
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
                    parsedMsg, chat_id = messager.parse_command()
                    if(not parsedMsg):
                        self.bot.sendMessage(chat_id=chat_id, text='ok')
                        return 'ok'
                        
                    if parsedMsg["is_valid"]:
                        logging.debug("[webhook_handler] parsedMsg ", parsedMsg)
                        self.cmd_queue[parsedMsg["pair"][2:]] = parsedMsg
                        response = parsedMsg["pair"][2:] + "-" + parsedMsg["frame"][9:] + " accepted."
                        self.bot.sendMessage(chat_id=chat_id, text=response)
                    else:
                        logging.error("[Error] Request message wrong format")
                        self.bot.sendMessage(chat_id=chat_id, text=parsedMsg["err_msg"])
                else:
                    logging.error("[Error] Request method=", request.method)
            except Exception as e: # work on python 3.x
                logging.error('[Exception][webhook_handler]: '+ str(e))
                self.bot.sendMessage(chat_id=MY_CHAT_ID, text="Error:" + str(e))

            return 'ok'

        @self.https_app.route("/getMessage", methods=['GET'])
        def get_msg(self=self):
            result = dict()
            pair = request.args.get('pair')
            if(not pair):
                return Response(json.dumps({'status_message':'pair is required'}), status=400, mimetype='application/json')
            msg = self.cmd_queue.get(pair)
            if(msg):
                self.cmd_queue[pair] = None
                return Response(json.dumps({"status_message":"ok", "data": msg}), status=200, mimetype='application/json')
            else:
                return Response(json.dumps({"status_message":"no job found"}), status=200, mimetype='application/json')

        @self.https_app.route("/sendMessage", methods=['POST'])
        def send_msg(self=self):
            body = request.json
            print("[sendcmd] data: " + json.dumps(body))
            if not body:
                return Response(json.dumps({'status_message':'no body'}), status=400, mimetype='application/json')

            
            chat_id = body["chat_id"]
            if not chat_id:
                return 'None'

            if body["msg_type"] == "photo":
                self.bot.send_photo(chat_id=chat_id, photo=open(body["photo_uri"], 'rb'))
            elif body["msg_type"] == "txt":
                msg = body["data"] if body["code"] else body["status_message"]
                composed_message = body["from"] + "> " + msg
                self.bot.sendMessage(chat_id=chat_id, text=composed_message)
            elif body["msg_type"] == "json":
                obj = json.loads(body["data"])
                data_str = json.dumps(obj, indent=2)
                composed_message = body["from"] + "> " + data_str
                self.bot.sendMessage(chat_id=chat_id, text=composed_message)
            else:
                return Response(json.dumps({'status_message':'message type not supported'}), status=405, mimetype='application/json')
                
            return Response(json.dumps({'status_message':'ok'}), status=200, mimetype='application/json')

    def send_message(self, chat_id, result):
        self.bot.sendMessage(chat_id=chat_id, text=result)

    def run(self):
        logging.info("Please access https:<domain>/ to register webhook portal for udpates!")
        self.https_app.run(host='0.0.0.0', port='443', ssl_context=('ssl/public.pem', 'ssl/private.key'))
        #self.https_app.run(host='10.148.0.7', port='80')
        #self.https_app.run(host='0.0.0.0', port='443', ssl_context='adhoc')
