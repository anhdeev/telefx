#!/usr/bin/env python
import logging
from typing import Dict

from modules.common import *

class CmdParser(object):
    currentPair=enMarketPair.E_EURUSD.name
    currentTimeFrame=enTimeframe.E_PERIOD_M15.name

    def __init__(self, cmd):
        self.parsedMsg = cmd.split()
        self.length = len(self.parsedMsg)

        if(self.parsedMsg[0] == "/use" and self.length >=3):
            CmdParser.currentPair = enMarketPair["E_" + self.parsedMsg[1]].name
            CmdParser.currentTimeFrame = enTimeframe["E_PERIOD_" + self.parsedMsg[2]].name
            self.length = 0

    def getCmd(self):
        if(self.length == 0):
            return None

        return self.parsedMsg[0]

    def getArgs(self):
        if(self.length == 0):
            return None

        mandatory = [ele for ele in self.parsedMsg[1:self.length] if '=' not in ele]

        return mandatory

    def getOptionalArgs(self):
        if(self.length == 0):
            return None

        optionals = [ele for ele in self.parsedMsg[1:self.length] if '=' in ele]
        parsedOptionals = dict()
        for o in optionals:
            a = o.split('=')
            if(len(a) !=2):
                continue
            parsedOptionals[a[0]] = a[1]

        print(parsedOptionals)
        return parsedOptionals