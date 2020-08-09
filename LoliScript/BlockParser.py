from LoliScript.LineParser import ParseToken,line
import re
from Blocks.BlockParse import BlockParse
from Blocks.BlockRequest import BlockRequest
from Blocks.BlockKeycheck import BlockKeycheck
from Blocks.BlockFunction import BlockFunction
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
        # Init the block object here
        # For some reason it will not init a new object if it's called frin the dict
        block = block()
        block.FromLS(line.current)
        if block:
            block.Dict["label"] = label
            block.Dict["block_type"] = identifier
            return block
        else:
            # ERROR
            return False
    else:
        return None
    
