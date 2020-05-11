from enum import Enum

class enTeleCmd(Enum):
    E_TELECMD_INTIAL = 0
    E_TELECMD_BUY = 1
    E_TELECMD_SELL = 2
    E_TELECMD_CAPTURE = 3
    E_TELECMD_GENERAL_DISCOVER =4
    E_TELECMD_MAX = 9999