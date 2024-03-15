
from Models.BotData import BotData
from LoliScript.CommandParser import IsCommand
from LoliScript.CommandParser import Parse as ParseCommand
from LoliScript.BlockParser import IsBlock, Parse as ParseBlock

import re
def CompressedLines(config_text) -> list:
    i = 0
    isScript = False
    compressed = config_text.splitlines()
    while i < len(compressed) - 1 :
        if isScript == False and IsBlock(compressed[i]) and compressed[i + 1].startswith(" ") or compressed[i + 1].startswith("\t"):
            compressed[i] += " " + compressed[i + 1].strip()
            compressed.pop(i + 1)
        elif isScript == False and IsBlock(compressed[i]) and compressed[i + 1].startswith("! ") or compressed[i + 1].startswith("!\t"):
            compressed[i] += " " + compressed[i + 1][1:].strip()
            compressed.pop(i + 1)
        else:
            if compressed[i].startswith("BEGIN SCRIPT"):
                isScript = True
            elif compressed[i].startswith("END SCRIPT"):
                isScript = False

            i += 1
    return compressed

class LoliScript():
    def __init__(self, script:str) -> None:
        self.i = 0
        self.lines: list[str] = []
        self.script = script
    def CanProceed(self):
        return self.i < len(self.lines)
    
    def reset(self):
        self.i = 0

        self.lines = re.split('\r\n|\r|\n', self.script)

    def IsEmptyOrCommentOrDisabled(self, line:str) -> bool:
        return line.strip() == "" or line.strip().startswith("##") or line.strip().startswith("!")

    def TakeStep(self, data:BotData):
        
        if data.status != BotData.BotStatus.NONE and data.status != BotData.BotStatus.SUCCESS and data.status != BotData.BotStatus.CUSTOM:
            self.i = len(self.lines)
            return

        currentLine = self.lines[self.i]

        while self.IsEmptyOrCommentOrDisabled(currentLine):
            self.i += 1
            currentLine = self.lines[self.i]

        lookahead = 0

        while self.i + 1 + lookahead < len(self.lines):
            nextline = self.lines[self.i + 1 + lookahead]
            if nextline.startswith(" ") or nextline.startswith("\t"):
                currentLine += nextline.lstrip()
            else:
                break

            lookahead += 1

        if IsBlock(currentLine):
            block = None

            block = ParseBlock(currentLine)

            CurrentBlock = block.label

            block.Process(data)
        elif IsCommand(currentLine):
            ac7ion = ParseCommand(currentLine, data) # Executes a command
        self.i += 1 + lookahead