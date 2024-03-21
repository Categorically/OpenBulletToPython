from LoliScript.LineParser import LineParser, ParseLabel, \
    ParseEnum, ParseLiteral, Lookahead, SetBool, ParseToken, \
    ParseInt, EnsureIdentifier
from Blocks.BlockBase import ReplaceValuesRecursive, \
    InsertVariable, ReplaceValues
from Functions.Encoding.Encode import ToBase64, \
    FromBase64
from Functions.Crypto.Crypto import Crypto
from Functions.UserAgent.UserAgent import UserAgent
from Extensions import Unescape
from urllib.parse import quote, unquote
from datetime import datetime
from datetime import timezone
import base64
import re
from random import randint
import random
import time
import math
from enum import Enum
from Models.CVar import CVar
from html import escape, unescape

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
                except Exception:
                    print("Failed to parse int")
                    return ""
                
                if padNum: randomNumString = randomNumString.rjust(len(str(maxNum)),"0")
                return randomNumString

                
class FunctionType(str, Enum):
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
        self.function_type = ""
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

        self.UserAgentBrowser = "Chrome"
        self.UserAgentSpecifyBrowser = False

        # PBKDF2PKCS5
        self.KdfSalt = ""
        self.KdfSaltSize = 8
        self.KdfIterations = 1
        self.KdfKeySize = 16
        self.KdfAlgorithm = "SHA1"

        # Translate
        self.TranslationDictionary = {}
        self.StopAfterFirstMatch = True
    def FromLS(self,line:LineParser):

        if str(line.current).startswith("!"):
            return None

        self.Dict = {} 

        self.Dict["IsCapture"] = False
        
        self.Dict["VariableName"] = ""

        self.Dict["InputString"] = ""

        self.Dict["Booleans"] = {}

        function_type  = ParseEnum(line)
        self.Dict["function_type"] = function_type
        self.function_type = function_type

        if function_type == FunctionType.Constant:
            pass

        elif function_type == FunctionType.Hash:
            HashType = ParseEnum(line)
            self.Dict["HashType"] = HashType
            self.HashType = HashType

            while Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif function_type == FunctionType.HMAC:
            HashType = ParseEnum(line)
            self.Dict["HashType"] = HashType
            self.HashType = HashType
            HmacKey = ParseLiteral(line)
            self.Dict["HmacKey"] = HmacKey
            self.HmacKey = HmacKey
            while Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif function_type == FunctionType.Translate:
            while Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
            self.Dict["TranslationDictionary"] = {}

            while line.current and Lookahead(line) == "Parameter":
                EnsureIdentifier(line, "KEY")
                k = ParseLiteral(line)
                EnsureIdentifier(line, "VALUE")
                v = ParseLiteral(line)
                self.Dict["TranslationDictionary"][k] = v
                self.TranslationDictionary[k] = v

        elif function_type == FunctionType.DateToUnixTime:
            self.Dict["DateFormat"] = ParseLiteral(line)

        elif function_type == FunctionType.UnixTimeToDate:
            DateFormat = ParseLiteral(line)
            self.DateFormat = DateFormat
            self.Dict["DateFormat"] = DateFormat
            if Lookahead(line) != "Literal":
                self.InputString = DateFormat
                self.DateFormat ="yyyy-MM-dd:HH-mm-ss"
                self.Dict["InputString"] = "yyyy-MM-dd:HH-mm-ss"

        elif function_type == FunctionType.Replace:
            ReplaceWhat = ParseLiteral(line)
            self.Dict["ReplaceWhat"] = ReplaceWhat
            self.ReplaceWhat = ReplaceWhat
            
            ReplaceWith = ParseLiteral(line)
            self.Dict["ReplaceWith"] = ReplaceWith
            self.ReplaceWith = ReplaceWith

            if Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif function_type == FunctionType.RegexMatch:
            self.Dict["RegexMatch"] = ParseLiteral(line)

        elif function_type == FunctionType.RandomNum:
            if Lookahead(line) == "Literal":
                RandomMin = ParseLiteral(line)
                RandomMax = ParseLiteral(line)
                self.Dict["RandomMin"] = RandomMin
                self.Dict["RandomMax"] = RandomMax
                self.RandomMin = RandomMin
                self.RandomMax = RandomMax
            # Support for old integer definition of Min and Max
            else:
                RandomMin = ParseLiteral(line)
                RandomMax = ParseLiteral(line)
                self.Dict["RandomMin"] = RandomMin
                self.Dict["RandomMax"] = RandomMax
                self.RandomMin = RandomMin
                self.RandomMax = RandomMax
            
            if Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif function_type == FunctionType.CountOccurrences:
            StringToFind = ParseLiteral(line)
            self.StringToFind = StringToFind
            self.Dict["StringToFind"] = StringToFind

        elif function_type == FunctionType.CharAt:
            charIndex = ParseLiteral(line)
            self.charIndex = charIndex
            self.Dict["CharIndex"] = charIndex

        elif function_type == FunctionType.Substring:
            SubstringIndex = ParseLiteral(line)
            SubstringLength = ParseLiteral(line)
            self.SubstringIndex = SubstringIndex
            self.SubstringLength = SubstringLength
            self.Dict["SubstringIndex"] = SubstringIndex
            self.Dict["SubstringLength"] = SubstringLength

        elif function_type == FunctionType.RSAEncrypt:
            self.Dict["RsaN"] = ParseLiteral(line)
            self.Dict["RsaE"] = ParseLiteral(line)
            if Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif function_type == FunctionType.RSAPKCS1PAD2:
            self.Dict["RsaN"] = ParseLiteral(line)
            self.Dict["RsaE"] = ParseLiteral(line)
        
        elif function_type == FunctionType.GetRandomUA:
            if ParseToken(line,"Parameter", False, False) == "BROWSER":
                EnsureIdentifier(line,"BROWSER")
                UserAgentBrowser = ParseEnum(line)
                self.UserAgentBrowser = UserAgentBrowser
                self.UserAgentSpecifyBrowser = True
                self.Dict["UserAgentBrowser"] = UserAgentBrowser
                self.Dict["Booleans"]["UserAgentSpecifyBrowser"] = True

        elif function_type == FunctionType.AESDecrypt:
            pass

        elif function_type == FunctionType.AESEncrypt:
            self.Dict["AesKey"] = ParseLiteral(line)
            self.Dict["AesIV"] = ParseLiteral(line)
            self.Dict["AesMode"] = ParseEnum(line)
            self.Dict["AesPadding"] = ParseEnum(line)

        elif function_type == FunctionType.PBKDF2PKCS5:
            if Lookahead(line) == "Literal":
                self.KdfSalt = ParseLiteral(line)
                self.KdfIterations = ParseInt(line)
                self.KdfKeySize = ParseInt(line)
                self.KdfAlgorithm = ParseEnum(line)
            else:
                self.KdfSaltSize = ParseInt(line)
                self.KdfIterations = ParseInt(line)
                self.KdfKeySize = ParseInt(line)
                self.KdfAlgorithm = ParseEnum(line)
        else:
            pass
        if Lookahead(line) == "Literal":
            inputString  = ParseLiteral(line)
            self.InputString = inputString
            self.Dict["InputString"] = inputString

        # Try to parse the arrow, otherwise just return the block as is with default var name and var / cap choice
        if not ParseToken(line,"Arrow",False,True):
            return self.Dict
            
        # Parse the VAR / CAP
        varType = ParseToken(line,"Parameter",True,True)
        if str(varType.upper()) == "VAR" or str(varType.upper()) == "CAP":
            if str(varType.upper()) == "CAP":
                self.Dict["IsCapture"] = True
                self.isCapture = True

        # Parse the variable/capture name
        VariableName = ParseToken(line,"Literal",True,True)
        self.VariableName = VariableName
        self.Dict["VariableName"] = VariableName

    def Process(self,BotData):
        localInputStrings = ReplaceValuesRecursive(self.InputString,BotData)
        outputs = []

        for localInputString in localInputStrings:
            # localInputString = localInputStrings[i]
            outputString = ""
            if self.function_type == FunctionType.Constant:
                outputString = localInputString

            elif self.function_type == FunctionType.Base64Encode:
                outputString = ToBase64(localInputString)

            elif self.function_type == FunctionType.Base64Decode:
                outputString = FromBase64(localInputString)

            elif self.function_type == FunctionType.Length:
                outputString = str(len(localInputString))

            elif self.function_type == FunctionType.ToLowercase:
                outputString = localInputString.lower()

            elif self.function_type == FunctionType.ToUppercase:
                outputString = localInputString.upper()

            elif self.function_type == FunctionType.Replace:
                if self.UseRegex:
                    outputString = re.sub(ReplaceValues(self.ReplaceWhat,BotData), ReplaceValues(self.ReplaceWith,BotData), localInputString)
                else:
                    outputString = localInputString.replace(ReplaceValues(self.ReplaceWhat,BotData),ReplaceValues(self.ReplaceWith,BotData))

            elif self.function_type == FunctionType.URLEncode:
                outputString = quote(localInputString,errors="replace")

            elif self.function_type == FunctionType.URLDecode:
                outputString = unquote(localInputString)

            elif self.function_type == FunctionType.Hash:
                outputString = self.GetHash(localInputString,self.HashType,self.InputBase64).lower()

            elif self.function_type == FunctionType.HMAC:
                 outputString = self.Hmac(localInputString,self.HashType,self.HmacKey,self.InputBase64,self.KeyBase64,self.HmacBase64)

            elif self.function_type == FunctionType.RandomNum:
                outputString = RandomNum(ReplaceValues(self.RandomMin,BotData),ReplaceValues(self.RandomMax,BotData),self.RandomZeroPad)

            elif self.function_type == FunctionType.RandomString:
                outputString = localInputString
                outputString = RandomString(outputString)

            elif self.function_type == FunctionType.CurrentUnixTime:
                outputString = str(int(time.time()))

            elif self.function_type == FunctionType.Ceil:
                outputString = str(math.ceil(float(localInputString)))

            elif self.function_type == FunctionType.Floor:
                outputString = str(math.floor(float(localInputString)))

            elif self.function_type == FunctionType.Round:
                outputString = str(round(float(localInputString)))

            elif self.function_type == FunctionType.CountOccurrences:
                outputString = str(localInputString.count(self.StringToFind))

            elif self.function_type == FunctionType.CharAt:
                outputString = str(localInputString[int(ReplaceValues(self.charIndex,BotData))])

            elif self.function_type == FunctionType.ReverseString:
                charArray = list(localInputString)
                charArray.reverse()
                outputString = "".join(charArray)

            elif self.function_type == FunctionType.Substring:
                outputString = localInputString[int(ReplaceValues(self.SubstringIndex,BotData)): int(ReplaceValues(self.SubstringIndex,BotData)) + int(ReplaceValues(self.SubstringLength, BotData))]

            elif self.function_type == FunctionType.GetRandomUA:
                if self.UserAgentSpecifyBrowser:
                    outputString = UserAgent.ForBrowser(self.UserAgentBrowser)
                else:
                    outputString = UserAgent.Random()

            elif self.function_type == FunctionType.Trim:
                outputString = localInputString.strip()

            elif self.function_type == FunctionType.UnixTimeToDate:
                # Static dateformat because dates
                outputString = datetime.fromtimestamp(int(localInputString),timezone.utc).strftime("%Y-%m-%d:%H-%M-%S")

            elif self.function_type == FunctionType.PBKDF2PKCS5:
                outputString = Crypto.PBKDF2PKCS5(localInputString, ReplaceValues(self.KdfSalt, BotData), self.KdfSaltSize, self.KdfIterations, self.KdfKeySize, self.KdfAlgorithm)

            elif self.function_type == FunctionType.Translate:
                outputString = localInputString
                for entryKey, entryValue in self.TranslationDictionary.items():
                    if entryKey in outputString:
                        outputString = outputString.replace(entryKey, entryValue)
                        if self.StopAfterFirstMatch: break
            elif self.function_type == FunctionType.Unescape:
                outputString = Unescape(localInputString)

            elif self.function_type == FunctionType.UnixTimeToISO8601:
                outputString = datetime.fromtimestamp(int(localInputString),timezone.utc).isoformat()

            elif self.function_type == FunctionType.ClearCookies:
                    BotData.CookiesSet(CVar("COOKIES",{},False,True))
            elif self.function_type == FunctionType.HTMLEntityEncode:
                outputString = escape(localInputString)
            elif self.function_type == FunctionType.HTMLEntityDecode:
                outputString = unescape(localInputString)
            else:
                pass
            outputs.append(outputString)

        print(f"Executed function {self.function_type} on input {localInputStrings} with outcome {outputString}")
        isList = len(outputs) > 1 or "[*]" in self.InputString or "(*)" in self.InputString or "{*}" in self.InputString
        InsertVariable(BotData,isCapture=self.IsCapture,recursive=isList,values=outputs,variableName=self.VariableName,createEmpty=self.CreateEmpty)

    def GetHash(self,baseString:str,hashAlg:str,inputBase64:bool):
        if not inputBase64:
            rawInput = baseString.encode('utf-8')
        else:
            try:
                rawInput = base64.b64decode(baseString.encode('utf-8'))
            except Exception:
                # In case the input is not base64 encoded
                return ""
        digest = bytearray()
        if hashAlg == "MD4":
            digest = Crypto.MD4(rawInput)
        elif hashAlg == "MD5":
            digest = Crypto.MD5(rawInput)
        elif hashAlg == "SHA1":
            digest = Crypto.SHA1(rawInput)
        elif hashAlg == "SHA256":
            digest = Crypto.SHA256(rawInput)
        elif hashAlg == "SHA384":
            digest = Crypto.SHA384(rawInput)
        elif hashAlg == "SHA512":
            digest = Crypto.SHA512(rawInput)
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
            signature  = Crypto.HMACMD5(rawInput,rawKey)

        elif hashAlg == "SHA1":
            signature  = Crypto.HMACSHA1(rawInput,rawKey)

        elif hashAlg == "SHA256":
            signature  = Crypto.HMACSHA256(rawInput,rawKey)

        elif hashAlg == "SHA384":
            signature  = Crypto.HMACSHA384(rawInput,rawKey)

        elif hashAlg == "SHA512":
            signature  = Crypto.HMACSHA512(rawInput,rawKey)
        else:
            return ""
        if outputBase64:
           return base64.b64encode(signature).decode("utf-8")
        else:
            return signature.hex().upper()
