#!/usr/bin/env python
import logging

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

        return self.parsedMsg[1:self.length-1]
