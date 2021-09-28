from OpenBullet2Python.LoliScript.LineParser import ParseToken,LineParser
import re
from OpenBullet2Python.Blocks.BlockParse import BlockParse
from OpenBullet2Python.Blocks.BlockRequest import BlockRequest
from OpenBullet2Python.Blocks.BlockKeycheck import BlockKeycheck
from OpenBullet2Python.Blocks.BlockFunction import BlockFunction
from OpenBullet2Python.Blocks.BlockUtility import BlockUtility
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

BlockMappings2  = {"BYPASSCF": None,
            "SOLVECAPTCHA": None,
            "REPORTCAPTCHA": None,
            "CAPTCHA": None,
            "FUNCTION": BlockFunction,
            "KEYCHECK": BlockKeycheck,
            "PARSE":BlockParse,
            "RECAPTCHA": None,
            "REQUEST": BlockRequest,
            "TCP": None,
            "UTILITY": BlockUtility,
            "BROWSERACTION": None,
            "ELEMENTACTION": None,
            "EXECUTEJS": None,
            "NAVIGATE": None}
def GetBlockType(line):
    try:
        return re.match('^!?(#[^ ]* )?([^ ]*)',line).group(2) 
    except Exception:
        return ""


def IsBlock(line) -> bool:
    if BlockMappings.get(GetBlockType(line)) == None:
        return False
    else:
        return True

def Parse(input_line):
    input_line = input_line.strip()
    line = LineParser()
    line.current = input_line

    disabled = input_line.startswith("!")
    if disabled: line.current[1:]

    label = ParseToken(line,"Label", False, True)
    
    identifier = ""
    identifier = ParseToken(line,"Parameter", True, True)

    # Get the class for the matching identifier
    block = BlockMappings2.get(identifier)
    #Todo blocks
    if block:
        # Init a new class
        block = block()
        block.FromLS(line)
        if block:
            block.label = label
            block.block_type = identifier
            return block
        else:
            # ERROR
            return False
    else:
        return None