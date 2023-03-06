from LoliScript.LineParser import LineParser, ParseLabel,ParseEnum,ParseLiteral,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier
from Blocks.BlockBase import ReplaceValues, ReplaceValuesRecursive
from Models.BotData import BotData
from Models.CVar import CVar
from Functions.Requests.Requests import OBRequest
from Functions.Requests.Requests import MultipartContent
from enum import Enum

def ParseString(input_string, separator, count) -> list:
    return [ n.strip() for n in input_string.split(separator,count)]
class RequestType(str, Enum):
    Standard = "Standard"
    BasicAuth = "BasicAuth"
    Multipart = "Multipart"
    Raw = "Raw"

class MultipartContentType(str, Enum):
    String = "String"
    File = "File"

class ResponseType(str, Enum):
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

        self.ContentType = ""

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

    def FromLS(self,line:LineParser):
        if str(line.current).startswith("!"):
            return None

        method = ParseEnum(line)
        self.method = method

        url = ParseLiteral(line)
        self.url = url

        while Lookahead(line) == "Boolean":
            boolean_name, boolean_value = SetBool(line,self)

        while len(str(line.current)) != 0 and line.current.startswith("->") == False:
            parsed = ParseToken(line,"Parameter",True,True).upper()
            if parsed == "MULTIPART":
                self.request_type = RequestType.Multipart

            elif parsed == "BASICAUTH":
                self.request_type = RequestType.BasicAuth

            elif parsed == "STANDARD":
                self.request_type = RequestType.Standard

            elif parsed == "RAW":
                self.request_type = RequestType.Raw

            elif parsed == "CONTENT":
                post_data = ParseLiteral(line)
                self.post_data = post_data

            elif parsed == "RAWDATA":
                raw_data = ParseLiteral(line)
                self.raw_data = raw_data

            elif parsed == "STRINGCONTENT":
                stringContentPair = ParseString(ParseLiteral(line), ':', 2)
                self.multipart_contents.append(MultipartContent(stringContentPair[0], stringContentPair[1], MultipartContentType.String))
                
            elif parsed == "FILECONTENT":
                fileContentTriplet = ParseString(ParseLiteral(line), ':', 3)
                self.multipart_contents.append(MultipartContent(fileContentTriplet[0], fileContentTriplet[1], MultipartContentType.File, fileContentTriplet[3]))

            elif parsed == "COOKIE":
                cookiePair = ParseString(ParseLiteral(line), ':', 2)
                self.custom_cookies[cookiePair[0]] = cookiePair[1]

            elif parsed == "HEADER":
                headerPair = ParseString(ParseLiteral(line), ':', 2)
                self.custom_headers[headerPair[0]] = headerPair[1]

            elif parsed == "CONTENTTYPE":
                ContentType = ParseLiteral(line)
                self.ContentType = ContentType

            elif parsed == "USERNAME":
                auth_user = ParseLiteral(line)
                self.auth_user = auth_user

            elif parsed == "PASSWORD":
                auth_pass = ParseLiteral(line)
                self.auth_pass = auth_pass

            elif parsed == "BOUNDARY":
                multipart_boundary = ParseLiteral(line)
                self.multipart_boundary = multipart_boundary

            elif parsed == "SECPROTO":
                SecurityProtocol = ParseLiteral(line)
                self.SecurityProtocol = SecurityProtocol

            else:
                pass

        if line.current.startswith("->"):
            EnsureIdentifier(line, "->")
            outType = ParseToken(line,"Parameter",True,True)

            if outType.upper() == "STRING":
                self.response_type = ResponseType.String

            elif outType.upper() == "FILE":
                self.response_type = ResponseType.File
                download_path  = ParseLiteral(line)
                self.download_path = download_path
                while Lookahead(line) == "Boolean":
                    boolean_name, boolean_value = SetBool(line,self)

            elif outType.upper() == "BASE64":
                self.response_type = ResponseType.Base64String
                output_variable = ParseLiteral(line)
                self.output_variable = output_variable
    def Process(self,BotData:BotData):
        proxy = BotData.proxy
        local_url = ReplaceValues(self.url,BotData)
        request = OBRequest()
        request.Setup(self.auto_redirect)

        if self.request_type == RequestType.Standard:
            request.SetStandardContent(ReplaceValues(self.post_data, BotData), ReplaceValues(self.ContentType, BotData), self.method, self.encode_content)
        elif self.request_type == RequestType.BasicAuth:
            request.SetBasicAuth(ReplaceValues(self.auth_user, BotData), ReplaceValues(self.auth_pass, BotData))
        elif self.request_type == RequestType.Raw:
            request.SetRawContent(ReplaceValues(self.raw_data, BotData), ReplaceValues(self.ContentType, BotData))
        elif self.request_type == RequestType.Multipart:
            contents = []
            for m in self.multipart_contents:
                contents.append(MultipartContent(
                    Name = ReplaceValues(m.Name, BotData),
                    Value = ReplaceValues(m.Value, BotData),
                    ContentType = ReplaceValues(m.ContentType, BotData),
                    Type = m.Type
                ))
            request.SetMultipartContent(contents, ReplaceValues(self.multipart_boundary, BotData))

            

        # Set request cookies
        cookies = {}
        cookieJar = BotData.CookiesGet()
        if cookieJar:
            cookies = cookieJar.Value

        for c in self.custom_cookies.items():
            cookies[ReplaceValues(c[0],BotData)] = cookies[ReplaceValues(c[1],BotData)]
        request.SetCookies(cookies)

        # Set request headers
        headers = {}
        for headerName, headerValue in self.custom_headers.items():
            headers[ReplaceValues(headerName,BotData)] = ReplaceValues(headerValue,BotData)
        request.SetHeaders(headers, self.accept_encoding)


        try:
            (Address, ResponseCode, ResponseHeaders, ResponseCookies) = request.Perform(self.url, self.method, proxy)
            print(f"{self.method} {local_url}")
        except Exception as e:
            print(e)
            return


        BotData.ResponseCodeSet(CVar("RESPONSECODE",ResponseCode,False,True))
        BotData.AddressSet(CVar("ADDRESS",Address,False,True))
        BotData.ResponseHeadersSet(CVar("HEADERS",ResponseHeaders,False,True))

        # Add response cookies to cookie jar
        for cN,cV in ResponseCookies.items():
            cookies[cN] = cV
        BotData.CookiesSet(CVar("COOKIES",cookies,False,True))

        if self.response_type == ResponseType.String:
            ResponseSource = request.SaveString(self.read_response_source, ResponseHeaders)
            BotData.ResponseSourceSet(CVar("SOURCE",ResponseSource,False,True))
                