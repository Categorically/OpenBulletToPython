from LoliScript.LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier
from Blocks.BlockBase import ReplaceValuesRecursive, InsertVariable,ReplaceValues
from Functions.Encoding.Encode import ToBase64, FromBase64
from urllib.parse import quote, unquote
import re
class Function:
    Constant = "Constant"
    Base64Encode = "Base64Encode"
    Base64Decode = "Base64Decode"
    Hash = "Hash"
    HMAC = "HMAC"
    Translate = "Translate"
    DateToUnixTime = "DateToUnixTime"
    Length = "Length"
    ToLowercase = "ToLowercase"
    ToUppercase = "ToUppercase"
    Replace = "Replace"
    RegexMatch = "RegexMatch"
    URLEncode = "URLEncode"
    URLDecode = "URLDecode"
    Unescape = "Unescape"
    HTMLEntityEncode = "HTMLEntityEncode"
    HTMLEntityDecode = "HTMLEntityDecode"
    UnixTimeToDate = "UnixTimeToDate"
    CurrentUnixTime = "CurrentUnixTime"
    UnixTimeToISO8601 = "UnixTimeToISO8601"
    RandomNum = "RandomNum"
    RandomString = "RandomString"
    Ceil = "Ceil"
    Floor = "Floor"
    Round = "Round"
    Compute = "Compute"
    CountOccurrences = "CountOccurrences"
    ClearCookies = "ClearCookies"
    RSAEncrypt = "RSAEncrypt"
    RSADecrypt = "RSADecrypt"
    RSAPKCS1PAD2 = "RSAPKCS1PAD2"
    Delay = "Delay"
    CharAt = "CharAt"
    Substring = "Substring"
    ReverseString = "ReverseString"
    Trim = "Trim"
    GetRandomUA = "GetRandomUA"
    AESEncrypt = "AESEncrypt"
    AESDecrypt = "AESDecrypt"
    PBKDF2PKCS5 = "PBKDF2PKCS5"

class BlockFunction:
    def __init__(self):
        self.VariableName = "" 
        self.IsCapture = False 
        self.InputString = "" 
        self.FunctionType = ""
        self.CreateEmpty = True
        self.Dict = {}
        self.UseRegex  = False
        
        # Replace
        self.ReplaceWhat = ""
        self.ReplaceWith = ""
    def FromLS(self,input_line):
        input_line = input_line.strip()

        if str(input_line).startswith("!"):
            return None
        line.current = input_line
        self.Dict = {} 

        self.Dict["IsCapture"] = False
        
        self.Dict["VariableName"] = ""

        self.Dict["InputString"] = ""

        self.Dict["Booleans"] = {}

        FunctionType  = ParseEnum(line.current)
        self.Dict["FunctionType"] = FunctionType
        self.FunctionType = FunctionType

        if FunctionType == Function().Constant:
            pass

        elif FunctionType == Function().Hash:
            HashType = ParseEnum(line.current)
            self.Dict["HashType"] = HashType

            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif FunctionType == Function().HMAC:
            self.Dict["HashType"] = ParseEnum(line.current)
            self.Dict["HmacKey"] = ParseLiteral(line.current)
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif FunctionType == Function().Translate:
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
            self.Dict["TranslationDictionary"] = {}
            while line.current and Lookahead(line.current) == "Parameter":
                EnsureIdentifier(line.current, "KEY")
                k = ParseLiteral(line.current)
                EnsureIdentifier(line.current, "VALUE")
                v = ParseLiteral(line.current)
                self.Dict["TranslationDictionary"][k] = v

        elif FunctionType == Function().DateToUnixTime:
            self.Dict["DateFormat"] = ParseLiteral(line.current)

        elif FunctionType == Function().UnixTimeToDate:
            self.Dict["DateFormat"] = ParseLiteral(line.current)
            if Lookahead(line.current) != "Literal":
                self.Dict["InputString"] = "yyyy-MM-dd:HH-mm-ss"

        elif FunctionType == Function().Replace:
            ReplaceWhat = ParseLiteral(line.current)
            self.Dict["ReplaceWhat"] = ReplaceWhat
            self.ReplaceWhat = ReplaceWhat
            
            ReplaceWith = ParseLiteral(line.current)
            self.Dict["ReplaceWith"] = ReplaceWith
            self.ReplaceWith = ReplaceWith

            if Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif FunctionType == Function().RegexMatch:
            self.Dict["RegexMatch"] = ParseLiteral(line.current)

        elif FunctionType == Function().RandomNum:
            if Lookahead(line.current) == "Literal":
                self.Dict["RandomMin"] = ParseLiteral(line.current)
                self.Dict["RandomMax"] = ParseLiteral(line.current)
            # Support for old integer definition of Min and Max
            else:
                self.Dict["RandomMin"] = str(ParseInt(line.current))
                self.Dict["RandomMax"] = str(ParseInt(line.current))
            
            if Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif FunctionType == Function().CountOccurrences:
            self.Dict["StringToFind"] = ParseLiteral(line.current)

        elif FunctionType == Function().CharAt:
            self.Dict["CharIndex"] = ParseLiteral(line.current)

        elif FunctionType == Function().Substring:
            self.Dict["SubstringIndex"] = ParseLiteral(line.current)
            self.Dict["SubstringLength"] = ParseLiteral(line.current)

        elif FunctionType == Function().RSAEncrypt:
            self.Dict["RsaN"] = ParseLiteral(line.current)
            self.Dict["RsaE"] = ParseLiteral(line.current)
            if Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif FunctionType == Function().RSAPKCS1PAD2:
            self.Dict["RsaN"] = ParseLiteral(line.current)
            self.Dict["RsaE"] = ParseLiteral(line.current)
        
        elif FunctionType == Function().GetRandomUA:
            if ParseToken(line.current,"Parameter", False, False) == "BROWSER":
                EnsureIdentifier(line.current,"BROWSER")
                self.Dict["Booleans"]["UserAgentSpecifyBrowser"] = True
                self.Dict["UserAgentBrowser"] = ParseEnum(line.current)

        elif FunctionType == Function().AESDecrypt:
            pass

        elif FunctionType == Function().AESEncrypt:
            self.Dict["AesKey"] = ParseLiteral(line.current)
            self.Dict["AesIV"] = ParseLiteral(line.current)
            self.Dict["AesMode"] = ParseEnum(line.current)
            self.Dict["AesPadding"] = ParseEnum(line.current)

        elif FunctionType == Function().PBKDF2PKCS5:
            if Lookahead(line.current) == "Literal":
                self.Dict["KdfSalt"] = ParseLiteral(line.current)
            else:
                self.Dict["KdfSaltSize"] = ParseInt(line.current)
                self.Dict["KdfIterations"] = ParseInt(line.current)
                self.Dict["KdfKeySize"] = ParseInt(line.current)
                self.Dict["KdfAlgorithm"] = ParseEnum(line.current)
                
        else:
            pass
        if Lookahead(line.current) == "Literal":
            inputString  = ParseLiteral(line.current)
            self.InputString = inputString
            self.Dict["InputString"] = inputString

        # Try to parse the arrow, otherwise just return the block as is with default var name and var / cap choice
        if not ParseToken(line.current,"Arrow",False,True):
            return self.Dict
            
        # Parse the VAR / CAP
        varType = ParseToken(line.current,"Parameter",True,True)
        if str(varType.upper()) == "VAR" or str(varType.upper()) == "CAP":
            if str(varType.upper()) == "CAP":
                self.Dict["IsCapture"] = True
                self.isCapture = True

        # Parse the variable/capture name
        VariableName = ParseToken(line.current,"Literal",True,True)
        self.VariableName = VariableName
        self.Dict["VariableName"] = VariableName

    def Process(self):
        localInputStrings = ReplaceValuesRecursive(self.InputString)
        outputs = []

        i = 0
        while i < len(localInputStrings):
            localInputString = localInputStrings[i]
            outputString = ""
            if self.FunctionType == "Constant":
                outputString = localInputString
            elif self.FunctionType == "Base64Encode":
                outputString = ToBase64(localInputString)
            elif self.FunctionType == "Base64Decode":
                outputString = FromBase64(localInputString)
            elif self.FunctionType == "Length":
                outputString = str(len(localInputString))
            elif self.FunctionType == "ToLowercase":
                outputString = localInputString.lower()
            elif self.FunctionType == "ToUppercase":
                outputString = localInputString.upper()
            elif self.FunctionType == "Replace":
                if self.UseRegex:
                    pass
                else:
                    outputString = localInputString.replace(ReplaceValues(self.ReplaceWhat),ReplaceValues(self.ReplaceWith))
            elif self.FunctionType == "URLEncode":
                outputString = quote(localInputString,errors="replace")

            elif self.FunctionType == "URLDecode":
                outputString = unquote(localInputString)
            else:
                pass
            outputs.append(outputString)
            i += 1
        print(f"Executed function {self.FunctionType} on input {localInputStrings} with outcome {outputString}")
        isList = len(outputs) > 1 or "[*]" in self.InputString or "(*)" in self.InputString or "{*}" in self.InputString
        InsertVariable(self.IsCapture,isList,outputs,self.VariableName,self.CreateEmpty)

