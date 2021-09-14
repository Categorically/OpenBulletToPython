
from OpenBullet2Python.LoliScript.Loliscript import CompressedLines

from OpenBullet2Python.LoliScript.BlockParser import Parse


def process_blocks(configtext:list,BotData):

    blocksList = []
    compressed = CompressedLines(configtext)
    for c in compressed:
        block = Parse(c)
        if block: blocksList.append(block)

    for block in blocksList:
        if BotData.status.value == BotData.BotStatus.FAIL or BotData.status.value == BotData.BotStatus.BAN or BotData.status.value == BotData.BotStatus.ERROR:
            return
        block.Process(BotData)
        
    
def ToPython(config_text):
    blocks = []
    compressed = CompressedLines(config_text)
    for c in compressed:
        c = Parse(c)
        if c: blocks.append(c.Dict)
    return blocks