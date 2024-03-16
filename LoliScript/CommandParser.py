from LoliScript.LineParser import ParseToken,LineParser
from enum import Enum
import re
from LoliScript.SetParser import Parse as ParseSet
from LoliScript.DeleteParser import Parse as ParseDelete
from Models.BotData import BotData

class CommandName(str, Enum):
    SET = "SET"
    DELETE = "DELETE"

def IsCommand(text):
    match = re.match("^([^ ]*)" , text)
    if not match:
        return False
    
    groups = match.groups()
    return any([group == command for command in CommandName for group in groups])

def Parse(input_line, data:BotData):
    input_line = input_line.strip()
    line = LineParser()
    line.current = input_line

    label = ParseToken(line,"Label", False, True)

    identifier = ""
    identifier = ParseToken(line,"Parameter", True, True)

    if identifier == CommandName.SET:
        return ParseSet(line, data)
    elif identifier == CommandName.DELETE:
        return ParseDelete(line, data)
            
