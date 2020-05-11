from enum import Enum

class enTeleCmd(Enum):
    E_TELECMD_INTIAL = 0
    E_TELECMD_BUY = 1
    E_TELECMD_SELL = 2
    E_TELECMD_CAPTURE = 3
    E_TELECMD_GENERAL_DISCOVER =4
    E_TELECMD_MAX = 9999

 

class enTimeframe(Enum):
    E_PERIOD_CURRENT
    E_PERIOD_M1
    E_PERIOD_M5
    E_PERIOD_M15
    E_PERIOD_M30
    E_PERIOD_H1
    E_PERIOD_H4
    E_PERIOD_D1
    E_PERIOD_W1
    E_PERIOD_MN1

class enMarketPair(Enum):
    E_PAIR_INITIAL
    E_EURUSD
    E_GBPUSD
    E_USDJPY
    E_USDCAD
    E_USDCHF
    E_NZDUSD
    E_EURSGD
    E_GBPJPY
    E_EURCAD
    E_EURJPY
    E_GBPCHF
    E_CADJPY
    E_AUDCHF
    E_NZDCHF
    E_CADCHF
    E_CHFJPY
    E_EURCHF
    E_EURGBP
    E_GBPCAD
    E_XAUUSD
    E_WTIUSD
    E_DXY
    E_PAIR_MAX