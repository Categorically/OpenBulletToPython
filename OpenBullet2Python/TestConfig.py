
from OpenBullet2Python.Models.BotData import BotData

from OpenBullet2Python.LoliScript.Loliscript import CompressedLines

from OpenBullet2Python.LoliScript.BlockParser import Parse

from OpenBullet2Python.Models.CVar import CVar
def TestConfig(configtext:list,BotData):

    blocksList = []
    compressed = CompressedLines(configtext)
    for c in compressed:
        block = Parse(c)
        if block: blocksList.append(block)

    for block in blocksList:
        # print(block)
        if BotData.Status.value == BotData.BotStatus.FAIL or BotData.Status.value == BotData.BotStatus.BAN or BotData.Status.value == BotData.BotStatus.ERROR:
            return
        block.Process(BotData)
        
    
