from OpenBullet2Python.LoliScript.LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier
from OpenBullet2Python.Blocks.BlockBase import ReplaceValues, ReplaceValuesRecursive
from OpenBullet2Python.Models.BotData import BotData
from OpenBullet2Python.Models.CVar import CVar

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
    def __init__(self,url=None):
        self.url = url
        self.request_type = RequestType.Standard

        # Basic Auth
        self.auth_user = ""
        self.auth_pass = ""

        # Standard
        self.post_data = ""

        # Raw
        self.raw_data = ""

        self.method = "GET"

        self.custom_cookies = {}

        self.custom_headers = {}

        self.ContentType = "application/x-www-form-urlencoded"

        self.auto_redirect = True

        self.read_response_source = True

        self.encode_content = False

        self.accept_encoding = True

        self.multipart_boundary = ""

        self.multipart_contents = []

        self.response_type = ResponseType.String

        self.download_path = ""

        self.output_variable = ""

        self.save_as_screenshot = False

        self.request_timeout = 60

        self.Dict = {}

    def FromLS(self,input_line):
        input_line = input_line.strip()
        line.current = input_line
        multipart_contents = []
        custom_headers = {}
        custom_cookies = {}

        if str(input_line).startswith("!"):
            return None

        self.Dict = {}

        method = ParseEnum(line.current)
        self.Dict["method"] = method
        self.method = method

        url = ParseLiteral(line.current)
        self.Dict["url"] = url
        self.url = url

        self.Dict["Booleans"] = {}
        while Lookahead(line.current) == "Boolean":
            boolean_name, boolean_value = SetBool(line.current,self)
            self.Dict["Booleans"][boolean_name] = boolean_value

        while len(str(line.current)) != 0 and line.current.startswith("->") == False:
            parsed = ParseToken(line.current,"Parameter",True,True).upper()
            if parsed == "MULTIPART":
                self.Dict["request_type"] = "Multipart"

            elif parsed == "BASICAUTH":
                self.Dict["request_type"] = "BasicAuth"

            elif parsed == "STANDARD":
                self.Dict["request_type"] = "Standard"
                self.request_type = RequestType.Standard

            elif parsed == "RAW":
                self.Dict["request_type"] = "Raw"

            elif parsed == "CONTENT":
                post_data = ParseLiteral(line.current)
                self.Dict["post_data"] = post_data
                self.post_data = post_data

            elif parsed == "RAWDATA":
                raw_data = ParseLiteral(line.current)
                self.Dict["raw_data"] = raw_data

            elif parsed == "STRINGCONTENT":
                stringContentPair = ParseString(ParseLiteral(line.current), ':', 2)
                multipart_contents.append({"Type": "STRING","Name":stringContentPair[0],"Value": stringContentPair[1] })
                
            elif parsed == "FILECONTENT":
                stringContentPair = ParseString(ParseLiteral(line.current), ':', 3)
                multipart_contents.append({"Type": "FILE","Name":stringContentPair[0],"Value": stringContentPair[1] })

            elif parsed == "COOKIE":
                cookiePair = ParseString(ParseLiteral(line.current), ':', 2)
                custom_cookies[cookiePair[0]] = cookiePair[1]

            elif parsed == "HEADER":
                headerPair = ParseString(ParseLiteral(line.current), ':', 2)
                custom_headers[headerPair[0]] = headerPair[1]
                self.custom_headers[headerPair[0]] = headerPair[1]

            elif parsed == "CONTENTTYPE":
                ContentType = ParseLiteral(line.current)
                self.Dict["ContentType"] = ContentType
                self.ContentType = ContentType

            elif parsed == "USERNAME":
                auth_user = ParseLiteral(line.current)
                self.Dict["auth_user"] = auth_user
                self.auth_user = auth_user

            elif parsed == "PASSWORD":
                auth_pass = ParseLiteral(line.current)
                self.Dict["auth_pass"] = auth_pass
                self.auth_pass = auth_pass

            elif parsed == "BOUNDARY":
                multipart_boundary = ParseLiteral(line.current)
                self.Dict["multipart_boundary"] = multipart_boundary

            elif parsed == "SECPROTO":
                SecurityProtocol = ParseLiteral(line.current)
                self.Dict["SecurityProtocol"] = SecurityProtocol

            else:
                pass

        if line.current.startswith("->"):
            EnsureIdentifier(line.current, "->")
            outType = ParseToken(line.current,"Parameter",True,True)

            if outType.upper() == "STRING":
                self.response_type = ResponseType.string

            elif outType.upper() == "FILE":
                self.response_type = ResponseType.file
                download_path  = ParseLiteral(line.current)
                self.Dict["download_path"] = download_path
                while Lookahead(line.current) == "Boolean":
                        
                    boolean_name, boolean_value = SetBool(line.current,self)
                    self.Dict["Booleans"][boolean_name] = boolean_value

            elif outType.upper() == "BASE64":
                self.response_type = ResponseType.Base64String
                output_variable = ParseLiteral(line.current)
                self.Dict["output_variable"] = output_variable
                
        self.Dict["custom_cookies"] = custom_cookies
        self.Dict["custom_headers"] = custom_headers
    # Using requests https://pypi.org/project/requests/ 
    # https://requests.readthedocs.io/en/master/
    def Process(self,BotData):
        cookies = BotData.CookiesGet()
        if cookies:
            cookies = cookies.Value
        else:
            cookies = {}
        for c in self.custom_cookies.items():
            cookies[ReplaceValues(c[0],BotData)] = cookies[ReplaceValues(c[1],BotData)]

        # Headers to be used for the request
        headers = {}
        for h in self.custom_headers.items():
            replacedKey = h[0].replace("-","").lower()
            # Don't want brotli
            if replacedKey == "acceptencoding":
                headers["Accept"] = "*/*"
            else:
                headers[ReplaceValues(h[0],BotData)] = ReplaceValues(h[1],BotData)

        # Add the content type to headers if ContentType is not null
        if self.ContentType:
            headers["Content-Type"] = self.ContentType
        local_url = ReplaceValues(self.url,BotData)
        if self.request_type == RequestType.Standard or self.request_type == RequestType.BasicAuth:
            username = ReplaceValues(self.auth_user,BotData)
            password = ReplaceValues(self.auth_pass,BotData)
            s = Session()
            try:
                if self.method in ["GET","HEAD","DELETE"]:
                    print(f"{self.method} {local_url}")

                    if self.request_type == RequestType.BasicAuth:
                        req = Request(self.method,  url=local_url, headers=headers,cookies=cookies,auth=(username,password))
                    else:
                        req = Request(self.method,  url=local_url, headers=headers,cookies=cookies)
                    prepped = s.prepare_request(req)

                    req = s.send(prepped,timeout=self.request_timeout,allow_redirects=self.auto_redirect)

                elif self.method in ["POST","PUT","PATCH"]:
                    
                    pData = ReplaceValues(self.post_data,BotData).encode("UTF-8","replace")
                    if self.encode_content == True:
                        pData = requests.utils.quote(pData)
                    print(f"{self.method} {local_url}")

                    if self.request_type == RequestType.BasicAuth:
                        req = Request(self.method,  url=local_url,data=pData, headers=headers,cookies=cookies,auth=(username,password))
                    else:
                        req = Request(self.method,  url=local_url,data=pData, headers=headers,cookies=cookies)
                    prepped = s.prepare_request(req)

                    req = s.send(prepped,timeout=self.request_timeout,allow_redirects=self.auto_redirect)
            except Exception:
                return

            ResponseCode = str(req.status_code)
            BotData.ResponseCodeSet(CVar("RESPONSECODE",ResponseCode,False,True))
            Address = str(req.url)
            BotData.ResponseSourceSet(CVar("ADDRESS",Address,False,True))
            Responce_Headers = dict(req.headers)
            BotData.ResponseHeadersSet(CVar("HEADERS",Responce_Headers,False,True))
            Responce_Cookies = dict(req.cookies)
            cookies = BotData.CookiesGet()
            if cookies:
                cookies = cookies.Value
            else:
                cookies = {}
            for cN,cV in Responce_Cookies.items():
                cookies[cN] = cV
            BotData.CookiesSet(CVar("COOKIES",cookies,False,True))

            if self.response_type == ResponseType.String:
                ResponseSource = str(req.text)
                BotData.ResponseSourceSet(CVar("SOURCE",ResponseSource,False,True))
                