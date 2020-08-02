
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
