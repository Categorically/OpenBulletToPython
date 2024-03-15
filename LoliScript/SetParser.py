from LoliScript.LineParser import ParseToken,ParseLiteral
from Models.CVar import CVar
from Models.BotData import BotData
def Parse(line_input, data:BotData):
    # input_line = line_input.strip()

    field = ParseToken(line_input,"Parameter", True, True).upper()

    if field == "VAR":
        data.Variables.Set(CVar(ParseLiteral(line_input),
                                ParseLiteral(line_input), False, False))
    elif field == "CAP":
        data.Variables.Set(CVar(ParseLiteral(line_input),
                                ParseLiteral(line_input), True, False))
