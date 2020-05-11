#!/usr/bin/env python
import os
import json
import logging

from modules.common import enTeleCmd

MY_USER_NAME="Duong Anh"
MY_USER_ID="378106375"
MY_CHAT_ID="378106375"

class Messager(object):
    def __init__(self, update):
        self.update = update
        self.text = None
        self.from_user = None
        self.msg_type = None
        self.msg_id = None
        self.chat_id = None
        self.from_id = None

        logging.debug(json.loads(update.to_json()))

        if update.channel_post:
            channel_post = json.loads(update.channel_post.to_json())
            self.msg_type = "channel_post"
            if channel_post.get('text'):
                self.text = channel_post['text']
            if channel_post.get('from'):
                self.from_user = channel_post['from']
        elif update.message:
            message = json.loads(update.message.to_json())
            self.msg_type = "message"
            if message.get('text'):
                self.text = message['text']
            if message.get('from'):
                self.from_user = message['from']
            if message.get('message_id'):
                self.msg_id = message['message_id']
            if message.get('chat'):
                self.chat_id = message['chat'].get('id')
        else:
            logging.warn("The message is not in type of 'message' neither 'channel_post'")

    def parse_command(self):
        if self.text == None or self.text == "" or self.text[:1] != '/':
            return (None, None)

        if self.from_user:
            if str(self.from_user['id']) != MY_USER_ID:
                logging.debug("Send from anothers")
                result = self._encodeCmd(self.text)
                return (self.chat_id, result)
            elif self.msg_type == "message" and self.text:
                logging.debug("Send from me")
                result = self._encodeCmd(self.text, True)
                return (self.chat_id, result)
            elif self.msg_type == "channel_post":
                logging.debug("Execute channel_post type message")
            else:
                logging.debug("Execute unknown type message")
        else:
            return (MY_CHAT_ID, "Anonymous user is not allowed!")

        return (None, None)

    # Request format
    # CMD[0:7] Command 
    # CMD[8:15] Parameter 1
    # CMD[16:23] Parameter 2
    # CMD[24:31] Parameter 3
    def _encodeCmd(self, request, me=False):
        encodedCmd = 0
        msgs = request.split(' ')

        if len(msgs) == 0:
            return None

        BYTE0 = msgs[0]
        del msgs[0]

        if BYTE0 == "/buy" and me:
            encodedCmd += enTeleCmd.E_TELECMD_BUY.value
            encodedArgs = self._encodeArgumentBuy(msgs)
            if(encodedArgs):
                encodedCmd += encodedArgs
                return encodedCmd
        elif BYTE0 == "/sell" and me:
            encodedCmd += enTeleCmd.E_TELECMD_BUY.value
            encodedArgs = self._encodeArgumentSell(msgs)
            if(encodedArgs):
                encodedCmd += encodedArgs
                return encodedCmd
        elif BYTE0 == "/screenshot":
            encodedCmd += enTeleCmd.E_TELECMD_BUY.value
            encodedArgs = self._encodeArgumentScreenshot(msgs)
            if(encodedArgs):
                encodedCmd += encodedArgs
                return encodedCmd
        elif BYTE0 == "/discover":
            encodedCmd += enTeleCmd.E_TELECMD_BUY.value
            encodedArgs = self._encodeArgumentDiscover(msgs)
            if(encodedArgs):
                encodedCmd += encodedArgs
                return encodedCmd
        else:
            return None

        return None

    # /buy EURUSD M5 2
    def _encodeArgumentBuy(self, args):
        encodedArgs = 0

        try:
            encodedArgs += (enMarketPair["E_" + args[0]].value << 8)
            encodedArgs += (enTimeframe["E_PERIOD_" + args[1]].value << 16)
            encodedArgs += (int(args[2]) << 24)
            return encodedArgs
        except:
            print("[_encodeArgumentBuy] An exception occurred")
            return None

    def _encodeArgumentSell(self, args):
        return self._encodeArgumentBuy(self, args)

    # /screenshot EURUSD M5
    def _encodeArgumentScreenshot(self, args):
        encodedArgs = 0

        try:
            encodedArgs += (enMarketPair["E_" + args[0]].value << 8)
            encodedArgs += (enTimeframe["E_PERIOD_" + args[1]].value << 16)
            return encodedArgs
        except:
            print("[_encodeArgumentScreenshot] An exception occurred")
            return None

    # /discover H1
    def _encodeArgumentDiscover(self, args):
        encodedArgs = 0

        try:
            encodedArgs += (enMarketPair["E_" + args[0]].value << 8)
            encodedArgs += (enTimeframe["E_PERIOD_" + args[1]].value << 16)
            return encodedArgs
        except:
            print("[_encodeArgumentScreenshot] An exception occurred")
            return None