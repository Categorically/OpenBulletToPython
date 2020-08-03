from LineParser import ParseToken,line
import re
BlockMappings  = {"BYPASSCF":"BlockBypassCF" ,
             "SOLVECAPTCHA":"BlockSolveCaptcha" ,
             "REPORTCAPTCHA":"BlockReportCaptcha" ,
             "CAPTCHA":"BlockImageCaptcha" ,
             "FUNCTION":"BlockFunction" ,
             "KEYCHECK":"BlockKeycheck" ,
             "PARSE":"BlockParse" ,
             "RECAPTCHA":"BlockRecaptcha" ,
             "REQUEST":"BlockRequest" ,
             "TCP":"BlockTCP" ,
             "UTILITY":"BlockUtility" ,
             "BROWSERACTION":"SBlockBrowserAction" ,
             "ELEMENTACTION":"SBlockElementAction" ,
             "EXECUTEJS":"SBlockExecuteJS" ,
             "NAVIGATE":"SBlockNavigate"}

from BlockParse import BlockParse
from BlockRequest import BlockRequest
from BlockKeycheck import BlockKeycheck
BlockMappings2  = {"BYPASSCF": None,
            "SOLVECAPTCHA": None,
            "REPORTCAPTCHA": None,
            "CAPTCHA": None,
            "FUNCTION": None,
            "KEYCHECK": BlockKeycheck().FromLS,
            "PARSE":BlockParse().FromLS ,
            "RECAPTCHA": None,
            "REQUEST": BlockRequest().FromLS,
            "TCP": None,
            "UTILITY": None,
            "BROWSERACTION": None,
            "ELEMENTACTION": None,
            "EXECUTEJS": None,
            "NAVIGATE": None}
def GetBlockType(line):
    try:
        return re.match('^!?(#[^ ]* )?([^ ]*)',line).group(2) 
    except:
        return ""


def IsBlock(line) -> bool:
    if BlockMappings.get(GetBlockType(line)) == None:
        return False
    else:
        return True

def Parse(input_line):
    input_line = input_line.strip()
    line.current = input_line

    disabled = input_line.startswith("!")
    if disabled: line.current[1:]

    label = ParseToken(line.current,"Label", False, True)
    
    identifier = ""
    identifier = ParseToken(line.current,"Parameter", True, True)

    block = BlockMappings2.get(identifier)
    #Todo blocks
    if block:
        block = block(line.current)
        block["label"] = label
        block["block_type"] = identifier
        return block
    else:
        return None
    
