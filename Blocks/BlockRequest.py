from LoliScript.LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier
from Blocks.BlockBase import ReplaceValues
from Models.BotData import BotData
from Models.CVar import CVar

import requests
from requests import Timeout
from requests import Request, Session
def ParseString(input_string, separator, count) -> list:
    return [ n.strip() for n in input_string.split(separator,count)]
class RequestType:
    Standard = "Standard"
    BasicAuth = "BasicAuth"
    Multipart = "Multipart"
    Raw = "Raw"

class MultipartContentType:
    String = "String"
    File = "File"

class ResponseType:
    String = "String"
    File = "File"
    Base64String = "Base64String"



class BlockRequest:
    def __init__(self,Url=None):
        self.Url = Url
        self.RequestType = RequestType().Standard

        # Basic Auth
        self.AuthUser = ""
        self.AuthPass = ""

        # Standard
        self.PostData = ""

        # Raw
        self.RawData = ""

        self.Method = "GET"

        self.CustomCookies = {}

        self.CustomHeaders = {}

        self.ContentType = "application/x-www-form-urlencoded"

        self.AutoRedirect = True

        self.ReadResponseSource = True

        self.encodeContent = False

        self.AcceptEncoding = True

        self.MultipartBoundary = ""

        self.MultipartContents = []

        self.ResponseType = ResponseType().String

        self.DownloadPath = ""

        self.OutputVariable = ""

        self.SaveAsScreenshot = False

        self.RequestTimeout = 60

        self.AutoRedirect = True

        self.Dict = {}

    def FromLS(self,input_line):
        input_line = input_line.strip()
        line.current = input_line
        MultipartContents = []
        CustomHeaders = {}
        CustomCookies = {}
        ResponseType = "String"

        if str(input_line).startswith("!"):
            return None

        self.Dict = {}

        Method = ParseEnum(line.current)
        self.Dict["Method"] = Method
        self.Method = Method

        Url = ParseLiteral(line.current)
        self.Dict["Url"] = Url
        self.Url = Url

        self.Dict["Booleans"] = {}
        while Lookahead(line.current) == "Boolean":
            boolean_name, boolean_value = SetBool(line.current,self)
            self.Dict["Booleans"][boolean_name] = boolean_value

        while len(str(line.current)) != 0 and line.current.startswith("->") == False:
            parsed = ParseToken(line.current,"Parameter",True,True).upper()
            if parsed == "MULTIPART":
                self.Dict["RequestType"] = "Multipart"

            elif parsed == "BASICAUTH":
                self.Dict["RequestType"] = "BasicAuth"

            elif parsed == "STANDARD":
                self.Dict["RequestType"] = "Standard"
                self.RequestType = RequestType.Standard

            elif parsed == "RAW":
                self.Dict["RequestType"] = "Raw"

            elif parsed == "CONTENT":
                PostData = ParseLiteral(line.current)
                self.Dict["PostData"] = PostData
                self.PostData = PostData

            elif parsed == "RAWDATA":
                RawData = ParseLiteral(line.current)
                self.Dict["RawData"] = RawData

            elif parsed == "STRINGCONTENT":
                stringContentPair = ParseString(ParseLiteral(line.current), ':', 2)
                MultipartContents.append({"Type": "STRING","Name":stringContentPair[0],"Value": stringContentPair[1] })
                
            elif parsed == "FILECONTENT":
                stringContentPair = ParseString(ParseLiteral(line.current), ':', 3)
                MultipartContents.append({"Type": "FILE","Name":stringContentPair[0],"Value": stringContentPair[1] })

            elif parsed == "COOKIE":
                cookiePair = ParseString(ParseLiteral(line.current), ':', 2)
                CustomCookies[cookiePair[0]] = cookiePair[1]

            elif parsed == "HEADER":
                headerPair = ParseString(ParseLiteral(line.current), ':', 2)
                CustomHeaders[headerPair[0]] = headerPair[1]
                self.CustomHeaders[headerPair[0]] = headerPair[1]

            elif parsed == "CONTENTTYPE":
                ContentType = ParseLiteral(line.current)
                self.Dict["ContentType"] = ContentType
                self.ContentType = ContentType

            elif parsed == "USERNAME":
                AuthUser = ParseLiteral(line.current)
                self.Dict["AuthUser"] = AuthUser

            elif parsed == "PASSWORD":
                AuthPass = ParseLiteral(line.current)
                self.Dict["AuthUser"] = AuthPass


            elif parsed == "BOUNDARY":
                MultipartBoundary = ParseLiteral(line.current)
                self.Dict["MultipartBoundary"] = MultipartBoundary

            elif parsed == "SECPROTO":
                SecurityProtocol = ParseLiteral(line.current)
                self.Dict["SecurityProtocol"] = SecurityProtocol

            else:
                pass

        if line.current.startswith("->"):
            EnsureIdentifier(line.current, "->")
            outType = ParseToken(line.current,"Parameter",True,True)

            if outType.upper() == "STRING":
                ResponseType = "String"

            elif outType.upper() == "File":
                ResponseType = "FILE"
                DownloadPath  = ParseLiteral(line.current)
                self.Dict["DownloadPath"] = DownloadPath
                while Lookahead(line.current) == "Boolean":
                        
                    boolean_name, boolean_value = SetBool(line.current,self)
                    self.Dict["Booleans"][boolean_name] = boolean_value

            elif outType.upper() == "BASE64":
                ResponseType = "BASE64"
                OutputVariable = ParseLiteral(line.current)
                self.Dict["OutputVariable"] = OutputVariable
                
        self.Dict["CustomCookies"] = CustomCookies
        self.Dict["CustomHeaders"] = CustomHeaders
    # Using requests https://pypi.org/project/requests/ 
    # https://requests.readthedocs.io/en/master/
    def Process(self):
        cookies = BotData.Cookies().get()
        if cookies:
            cookies = cookies.Value
        else:
            cookies = {}
        for c in self.CustomCookies.items():
            cookies[ReplaceValues(c[0])] = cookies[ReplaceValues(c[1])]

        # Headers to be used for the request
        headers = {}
        for h in self.CustomHeaders.items():
            replacedKey = h[0].replace("-","").lower()
            # Don't want brotli
            if replacedKey == "acceptencoding":
                headers["Accept"] = "*/*"
            else:
                headers[ReplaceValues(h[0])] = ReplaceValues(h[1])

        # Add the content type to headers if ContentType is not null
        if self.ContentType:
            headers["Content-Type"] = self.ContentType
        localUrl = ReplaceValues(self.Url)
        if self.RequestType == RequestType().Standard:
            if self.Method in ["GET","HEAD","DELETE"]:
                print(f"{self.Method} {localUrl}")

                s = Session()
                req = Request(self.Method,  url=localUrl, headers=headers,cookies=cookies)
                prepped = s.prepare_request(req)
                try:
                    req = s.send(prepped,timeout=self.RequestTimeout,allow_redirects=self.AutoRedirect)
                except:
                    return

            elif self.Method in ["POST","PUT","PATCH"]:
                
                pData = ReplaceValues(self.PostData).encode("UTF-8","replace")
                if self.encodeContent == True:
                    pData = requests.utils.quote(pData)
                print(f"{self.Method} {localUrl}")

                s = Session()
                req = Request(self.Method,  url=localUrl,data=pData, headers=headers,cookies=cookies)
                prepped = s.prepare_request(req)
                try:
                    req = s.send(prepped,timeout=self.RequestTimeout,allow_redirects=self.AutoRedirect)
                except:
                    return
        

            ResponseCode = str(req.status_code)
            BotData.ResponseCode().set(CVar("RESPONSECODE",ResponseCode,False,True))
            Address = str(req.url)
            BotData.ResponseSource().set(CVar("ADDRESS",Address,False,True))
            Responce_Headers = dict(req.headers)
            BotData.ResponseHeaders().set(CVar("HEADERS",Responce_Headers,False,True))
            Responce_Cookies = dict(req.cookies)
            cookies = BotData.Cookies().get()
            if cookies:
                cookies = cookies.Value
            else:
                cookies = {}
            for cN,cV in Responce_Cookies.items():
                cookies[cN] = cV
            BotData.Cookies().set(CVar("COOKIES",cookies,False,True))

            if self.ResponseType == ResponseType().String:
                ResponseSource = str(req.text)
                BotData.ResponseSource().set(CVar("SOURCE",ResponseSource,False,True))
                