import re
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
def ParseLabel(line_input):
    return ParseToken(line_input,"Label",True,True)
def ParseLiteral(line_input):
    return ParseToken(line_input,"Literal",True,True)
def ParseEnum(line_input):
    return ParseToken(line_input,"Parameter",True,True)

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
    else:
        return "Parameter"

def SetBool(line_input):
    name, value  = ParseToken(line_input,"Parameter",True,True).split("=")
    return name, value