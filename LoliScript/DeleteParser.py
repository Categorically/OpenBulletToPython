from LoliScript.LineParser import ParseToken,ParseLiteral, Lookahead, ParseEnum
from Models.CVar import CVar
from Models.BotData import BotData
from Functions.Conditions.Condition import Comparer

def Parse(line_input, data:BotData):

    field = ParseToken(line_input,"Parameter", True, True).upper()
    comparer = Comparer.EqualTo;
    if field == "VAR":
        if Lookahead(line_input) == "Parameter":
            comparer = ParseEnum(line_input)
        name = ParseLiteral(line_input)
        data.Variables.RemoveWithComparer(comparer, name, data)