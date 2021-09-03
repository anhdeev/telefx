#!/usr/bin/env python
import os
import json
import logging

from modules.common import *
from modules.cmd_parser import *

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
            return dict()

        parser = CmdParser(self.text)
        if(not parser.getCmd()):
            return None

        parsedMsg = {
            "cmd": parser.getCmd(),
            "args": parser.getArgs(),
            "pair": parser.currentPair,
            "timeframe": parser.currentTimeFrame,
            #"from_user": self.from_user,
            "msg_type": self.msg_type,
            "msg_id": self.msg_id,
            "chat_id": self.chat_id,
            "from_id": self.from_id,
            "role": "normal",
            "is_valid": True,
            "err_msg": ""
        }

        if self.from_user:
            if str(self.from_user['id']) == MY_USER_ID:
                parsedMsg["role"] = "admin"

            if self.msg_type == "message" and self.text:
                pass
            elif self.msg_type == "channel_post":
                pass
            else:
                err_msg = "Execute unknown type message"
                logging.error(err_msg)
                parsedMsg["err_msg"] = err_msg
        else:
            err_msg = "Anonymous user is not allowed!"
            logging.error(err_msg)
            parsedMsg["err_msg"] = err_msg

        return parsedMsg
