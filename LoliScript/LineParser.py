import re

#Class is used as a replacement for ref
class line:
    current = ""


def GetPattern(TokenType):
    tokens = {"Label":'^#[^ ]*',
              "Parameter":'^[^ ]*',
              "Literal":'\"(\\\\.|[^\\\"])*\"',
              "Arrow":'->'}
    return tokens.get(TokenType)


def ParseToken(line_input,TokenType,essential,proceed):
    pattern = GetPattern(TokenType)
    token = ""
    r = re.compile(pattern)
    m = r.match(line_input)
    if m:
        token = m.group(0)
        if proceed:
            line.current = line_input[len(token):].strip()
        if TokenType == "Literal":
            token = token[1:len(token) - 1].replace("\\\\", "\\").replace("\\\"", "\"")
    else:
        if essential:
            pass
    return token


def ParseLabel(line_input) -> str:
    return ParseToken(line_input,"Label",True,True)


def ParseLiteral(line_input) -> str:
    return ParseToken(line_input,"Literal",True,True)

    
def ParseEnum(line_input) -> str:
    return ParseToken(line_input,"Parameter",True,True)


def ParseInt(line_input) -> int:
    try:
        return int(ParseToken(line_input,"Parameter",True,True))
    except:
        print("Expected Integer value")
        return 0



def Lookahead(line_input):
    token = ParseToken(line_input,"Parameter",True,False)
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


def SetBool(line_input,object):
    name, value  = ParseToken(line_input,"Parameter",True,True).split("=")
    if "TRUE" in value.upper():
        setattr(object,name,True)
    elif "FALSE" in value.upper():
        setattr(object,name,False)
    return name, value

def EnsureIdentifier(input_string, id_string):
    token = ParseToken(input_string,"Parameter",True,True)
    if token.upper() != id_string.upper():
        print(f"Expected identifier '{id_string}")

def CheckIdentifier(input_string, id_string):
    try:
        token = ParseToken(input_string,"Parameter",True,False)
        return token.upper() == id_string.upper()
    except:
        return False