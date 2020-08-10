
from Models.BotData import BotData

from LoliScript.Loliscript import CompressedLines

from LoliScript.BlockParser import Parse

from Models.CVar import CVar
def TestConfig(configtext:list):

    blocksList = []
    compressed = CompressedLines(configtext)
    for c in compressed:
        block = Parse(c)
        if block: blocksList.append(block)

    for block in blocksList:
        # print(block)
        if BotData.Status.value == BotData.BotStatus.FAIL or BotData.Status.value == BotData.BotStatus.BAN or BotData.Status.value == BotData.BotStatus.ERROR:
            return
        block.Process()
        
    
