
from OpenBullet2Python.LoliScript.Loliscript import CompressedLines

from OpenBullet2Python.LoliScript.BlockParser import Parse


def process_blocks(configtext:list,BotData):
    """
    Parse the config blocks

    Process the blocks

    Breaks on BotData.status
    """

    blocksList = []
    compressed = CompressedLines(configtext)
    for c in compressed:
        # Get the block class from the line
        block = Parse(c)
        if block: blocksList.append(block)

    for block in blocksList:
        if BotData.status.value == BotData.BotStatus.FAIL or BotData.status.value == BotData.BotStatus.BAN or BotData.status.value == BotData.BotStatus.ERROR:
            return
        # call the class method to process the block
        block.Process(BotData)
        

def ToPython(config_text):
    """
    Parse the config blocks

    Returns an array of block dicts
    """
    blocks = []
    compressed = CompressedLines(config_text)
    for c in compressed:
        c = Parse(c)
        if c: blocks.append(c.Dict)
    return blocks