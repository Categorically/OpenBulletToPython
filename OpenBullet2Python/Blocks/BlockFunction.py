from OpenBullet2Python.LoliScript.LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier
from OpenBullet2Python.Blocks.BlockBase import ReplaceValuesRecursive, InsertVariable,ReplaceValues
from OpenBullet2Python.Functions.Encoding.Encode import ToBase64, FromBase64
from OpenBullet2Python.Functions.Crypto.Crypto import Crypto
from urllib.parse import quote, unquote
import base64
import re
from random import randint
import random
def RandomString(localInputString:str):
    _lowercase = "abcdefghijklmnopqrstuvwxyz"
    _uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _digits = "0123456789"
    _symbols = "\\!\"£$%&/()=?^'{}[]@#,;.:-_*+"
    _hex = _digits + "abcdef"
    _udChars = _uppercase + _digits
    _ldChars = _lowercase + _digits
    _upperlwr = _lowercase + _uppercase
    _ludChars = _lowercase + _uppercase + _digits
    _allChars = _lowercase + _uppercase + _digits + _symbols
    outputString = localInputString
    if "?l" in str(outputString):
        while "?l" in str(outputString):
            outputString = outputString.replace("?l",random.choice(list(_lowercase)),1)
    if "?u" in str(outputString):
        while "?u" in str(outputString):
            outputString = outputString.replace("?u",random.choice(list(_uppercase)),1)
    if "?d" in str(outputString):
        while "?d" in str(outputString):
            outputString = outputString.replace("?d",random.choice(list(_digits)),1)
    if "?s" in str(outputString):
        while "?s" in str(outputString):
            outputString = outputString.replace("?s",random.choice(list(_symbols)),1)
    if "?h" in str(outputString):
        while "?h" in str(outputString):
            outputString = outputString.replace("?h",random.choice(list(_hex)),1)
    if "?a" in str(outputString):
        while "?a" in str(outputString):
            outputString = outputString.replace("?a",random.choice(list(_allChars)),1)
    if "?m" in str(outputString):
        while "?m" in str(outputString):
            outputString = outputString.replace("?m",random.choice(list(_udChars)),1)
    if "?n" in str(outputString):
        while "?n" in str(outputString):
            outputString = outputString.replace("?n",random.choice(list(_ldChars)),1)
    if "?i" in str(outputString):
        while "?i" in str(outputString):
            outputString = outputString.replace("?i",random.choice(list(_ludChars)),1)
    if "?f" in str(outputString):
        while "?f" in str(outputString):
            outputString = outputString.replace("?f",random.choice(list(_upperlwr)),1)
    return outputString

def RandomNum(minNum,maxNum,padNum:bool):
                try:
                    randomNumString = str(randint(int(minNum),int(maxNum)))
                except:
                    print("Failed to parse int")
                    return ""
                
                if padNum: randomNumString = randomNumString.rjust(len(str(maxNum)),"0")
                return randomNumString

                
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

        # Hashing 
        self.HashType = ""
        self.InputBase64 = False

        self.KeyBase64 = False
        self.HmacBase64 = False

        self.RandomZeroPad = False
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
            self.HashType = HashType

            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif FunctionType == Function().HMAC:
            HashType = ParseEnum(line.current)
            self.Dict["HashType"] = HashType
            self.HashType = HashType
            HmacKey = ParseLiteral(line.current)
            self.Dict["HmacKey"] = HmacKey
            self.HmacKey = HmacKey
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
                RandomMin = ParseLiteral(line.current)
                RandomMax = ParseLiteral(line.current)
                self.Dict["RandomMin"] = RandomMin
                self.Dict["RandomMax"] = RandomMax
                self.RandomMin = RandomMin
                self.RandomMax = RandomMax
            # Support for old integer definition of Min and Max
            else:
                RandomMin = ParseLiteral(line.current)
                RandomMax = ParseLiteral(line.current)
                self.Dict["RandomMin"] = RandomMin
                self.Dict["RandomMax"] = RandomMax
                self.RandomMin = RandomMin
                self.RandomMax = RandomMax
            
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

    def Process(self,BotData):
        localInputStrings = ReplaceValuesRecursive(self.InputString,BotData)
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
                    outputString = localInputString.replace(ReplaceValues(self.ReplaceWhat,BotData),ReplaceValues(self.ReplaceWith,BotData))

            elif self.FunctionType == "URLEncode":
                outputString = quote(localInputString,errors="replace")

            elif self.FunctionType == "URLDecode":
                outputString = unquote(localInputString)

            elif self.FunctionType == "Hash":
                outputString = self.GetHash(localInputString,self.HashType,self.InputBase64).lower()

            elif self.FunctionType == "HMAC":
                 outputString = self.Hmac(localInputString,self.HashType,self.HmacKey,self.InputBase64,self.KeyBase64,self.HmacBase64)
            elif self.FunctionType == "RandomNum":
                outputString = RandomNum(ReplaceValues(self.RandomMin,BotData),ReplaceValues(self.RandomMax,BotData),self.RandomZeroPad)
            elif self.FunctionType == "RandomString":
                outputString = localInputString
                outputString = RandomString(outputString)
            else:
                pass
            outputs.append(outputString)
            i += 1
        print(f"Executed function {self.FunctionType} on input {localInputStrings} with outcome {outputString}")
        isList = len(outputs) > 1 or "[*]" in self.InputString or "(*)" in self.InputString or "{*}" in self.InputString
        InsertVariable(BotData,self.IsCapture,isList,outputs,self.VariableName,self.CreateEmpty)

    def GetHash(self,baseString:str,hashAlg:str,inputBase64:bool):
        if not inputBase64:
            rawInput = baseString.encode('utf-8')
        else:
            try:
                rawInput = base64.b64decode(baseString.encode('utf-8'))
            except:
                # In case the input is not base64 encoded
                return ""
        digest = bytearray()
        if hashAlg == "MD5":
            digest = Crypto().MD5(rawInput)
        elif hashAlg == "SHA1":
            digest = Crypto().SHA1(rawInput)
        elif hashAlg == "SHA256":
            digest = Crypto().SHA256(rawInput)
        elif hashAlg == "SHA384":
            digest = Crypto().SHA384(rawInput)
        elif hashAlg == "SHA512":
            digest = Crypto().SHA512(rawInput)
        return digest.hex()

    def Hmac(self, baseString:str,hashAlg,key:str,inputBase64:bool,keyBase64:bool,outputBase64:bool):
        rawInput = bytearray()
        rawKey = bytearray()
        signature = bytearray()
        if inputBase64:
            rawInput = base64.b64decode(baseString.encode('utf-8'))
        else:
            rawInput = baseString.encode('utf-8')

        if keyBase64:
            rawKey = base64.b64decode(key.encode('utf-8'))
        else:
            rawKey = key.encode('utf-8')

        if hashAlg == "MD5":
            signature  = Crypto().HMACMD5(rawInput,rawKey)

        elif hashAlg == "SHA1":
            signature  = Crypto().HMACSHA1(rawInput,rawKey)

        elif hashAlg == "SHA256":
            signature  = Crypto().HMACSHA256(rawInput,rawKey)

        elif hashAlg == "SHA384":
            signature  = Crypto().HMACSHA384(rawInput,rawKey)

        elif hashAlg == "SHA512":
            signature  = Crypto().HMACSHA512(rawInput,rawKey)
        else:
            return ""
        if outputBase64:
           return base64.b64encode(signature).decode("utf-8")
        else:
            return signature.hex().upper()
