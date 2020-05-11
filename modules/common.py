from enum import Enum

class enTeleCmd(Enum):
    E_TELECMD_INTIAL = 0
    E_TELECMD_BUY = 1
    E_TELECMD_SELL = 2
    E_TELECMD_CAPTURE = 3
    E_TELECMD_GENERAL_DISCOVER =4
    E_TELECMD_MAX = 9999

 

class enTimeframe(Enum):
    E_PERIOD_CURRENT = 0
    E_PERIOD_M1 = 1
    E_PERIOD_M5 = 2
    E_PERIOD_M15 = 3
    E_PERIOD_M30 = 4
    E_PERIOD_H1 = 5
    E_PERIOD_H4 = 6
    E_PERIOD_D1 = 7
    E_PERIOD_W1 = 8
    E_PERIOD_MN1 = 9

class enMarketPair(Enum):
    E_PAIR_INITIAL = 0
    E_EURUSD = 1
    E_GBPUSD = 2
    E_USDJPY = 3
    E_USDCAD = 4
    E_USDCHF = 5
    E_NZDUSD = 6
    E_EURSGD = 7
    E_GBPJPY = 8
    E_EURCAD = 9
    E_EURJPY = 10
    E_GBPCHF = 11
    E_CADJPY = 12
    E_AUDCHF = 13
    E_NZDCHF = 14
    E_CADCHF = 15
    E_CHFJPY = 16
    E_EURCHF = 17
    E_EURGBP = 18
    E_GBPCAD = 19
    E_XAUUSD = 20
    E_WTIUSD = 21
    E_DXY = 22
    E_PAIR_MAX = 9999