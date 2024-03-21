import re
from Models.BotData import BotData
from Blocks.BlockBase import ReplaceValues
class LineParser:
    def __init__(self) -> None:
        self.current = ""


def GetPattern(TokenType):
    tokens = {"Label":'^#[^ ]*',
              "Parameter":'^[^ ]*',
              "Literal":'\"(\\\\.|[^\\\"])*\"',
              "Arrow":'->'}
    return tokens.get(TokenType)


def ParseToken(line:LineParser,TokenType,essential,proceed):
    pattern = GetPattern(TokenType)
    token = ""
    r = re.compile(pattern)
    m = r.match(line.current)
    if m:
        token = m.group(0)
        if proceed:
            line.current = line.current[len(token):].strip()
        if TokenType == "Literal":
            token = token[1:len(token) - 1].replace("\\\\", "\\").replace("\\\"", "\"")
    else:
        if essential:
            pass
    return token


def ParseLabel(line:LineParser) -> str:
    return ParseToken(line,"Label",True,True)


def ParseLiteral(line:LineParser,replace=False, data:BotData = None) -> str:
    if replace:
        return ReplaceValues(line.current, data)
    return ParseToken(line,"Literal",True,True)

    
def ParseEnum(line:LineParser) -> str:
    return ParseToken(line,"Parameter",True,True)


def ParseInt(line:LineParser) -> int:
    try:
        return int(ParseToken(line,"Parameter",True,True))
    except Exception:
        print("Expected Integer value")
        return 0



def Lookahead(line:LineParser):
    token = ParseToken(line,"Parameter",True,False)
    if '\"' in token:
        return "Literal"
    elif '->' in token:
        return "Arrow"
    elif token.startswith("#"):
        return "Label"
    elif "=TRUE" in token.upper() or "=FALSE" in token.upper():
        return "Boolean"
    elif token.isdigit():
        return "Integer"
    else:
        return "Parameter"


def SetBool(line:LineParser,object):
    name, value  = ParseToken(line,"Parameter",True,True).split("=")
    if "TRUE" in value.upper():
        setattr(object,name,True)
    elif "FALSE" in value.upper():
        setattr(object,name,False)
    return name, value

def EnsureIdentifier(line:LineParser, id_string):
    token = ParseToken(line,"Parameter",True,True)
    if token.upper() != id_string.upper():
        print(f"Expected identifier '{id_string}")

def CheckIdentifier(line:LineParser, id_string):
    try:
        token = ParseToken(line,"Parameter",True,False)
        return token.upper() == id_string.upper()
    except Exception:
        return False