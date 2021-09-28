from OpenBullet2Python.LoliScript.LineParser import LineParser, ParseLabel,ParseEnum,ParseLiteral,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier
from OpenBullet2Python.Blocks.BlockBase import ReplaceValues, ReplaceValuesRecursive
from OpenBullet2Python.Models.BotData import BotData
from OpenBullet2Python.Models.CVar import CVar
from OpenBullet2Python.Functions.Requests.Requests import OBRequest

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

        self.Dict = {}

    def FromLS(self,line:LineParser):
        
        multipart_contents = []
        custom_headers = {}
        custom_cookies = {}

        if str(line.current).startswith("!"):
            return None

        self.Dict = {}

        method = ParseEnum(line)
        self.Dict["method"] = method
        self.method = method

        url = ParseLiteral(line)
        self.Dict["url"] = url
        self.url = url

        self.Dict["Booleans"] = {}
        while Lookahead(line) == "Boolean":
            boolean_name, boolean_value = SetBool(line,self)
            self.Dict["Booleans"][boolean_name] = boolean_value

        while len(str(line.current)) != 0 and line.current.startswith("->") == False:
            parsed = ParseToken(line,"Parameter",True,True).upper()
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
                post_data = ParseLiteral(line)
                self.Dict["post_data"] = post_data
                self.post_data = post_data

            elif parsed == "RAWDATA":
                raw_data = ParseLiteral(line)
                self.Dict["raw_data"] = raw_data

            elif parsed == "STRINGCONTENT":
                stringContentPair = ParseString(ParseLiteral(line), ':', 2)
                multipart_contents.append({"Type": "STRING","Name":stringContentPair[0],"Value": stringContentPair[1] })
                
            elif parsed == "FILECONTENT":
                stringContentPair = ParseString(ParseLiteral(line), ':', 3)
                multipart_contents.append({"Type": "FILE","Name":stringContentPair[0],"Value": stringContentPair[1] })

            elif parsed == "COOKIE":
                cookiePair = ParseString(ParseLiteral(line), ':', 2)
                custom_cookies[cookiePair[0]] = cookiePair[1]

            elif parsed == "HEADER":
                headerPair = ParseString(ParseLiteral(line), ':', 2)
                custom_headers[headerPair[0]] = headerPair[1]
                self.custom_headers[headerPair[0]] = headerPair[1]

            elif parsed == "CONTENTTYPE":
                ContentType = ParseLiteral(line)
                self.Dict["ContentType"] = ContentType
                self.ContentType = ContentType

            elif parsed == "USERNAME":
                auth_user = ParseLiteral(line)
                self.Dict["auth_user"] = auth_user
                self.auth_user = auth_user

            elif parsed == "PASSWORD":
                auth_pass = ParseLiteral(line)
                self.Dict["auth_pass"] = auth_pass
                self.auth_pass = auth_pass

            elif parsed == "BOUNDARY":
                multipart_boundary = ParseLiteral(line)
                self.Dict["multipart_boundary"] = multipart_boundary

            elif parsed == "SECPROTO":
                SecurityProtocol = ParseLiteral(line)
                self.Dict["SecurityProtocol"] = SecurityProtocol

            else:
                pass

        if line.current.startswith("->"):
            EnsureIdentifier(line, "->")
            outType = ParseToken(line,"Parameter",True,True)

            if outType.upper() == "STRING":
                self.response_type = ResponseType.string

            elif outType.upper() == "FILE":
                self.response_type = ResponseType.file
                download_path  = ParseLiteral(line)
                self.Dict["download_path"] = download_path
                while Lookahead(line) == "Boolean":
                        
                    boolean_name, boolean_value = SetBool(line,self)
                    self.Dict["Booleans"][boolean_name] = boolean_value

            elif outType.upper() == "BASE64":
                self.response_type = ResponseType.Base64String
                output_variable = ParseLiteral(line)
                self.Dict["output_variable"] = output_variable
                
        self.Dict["custom_cookies"] = custom_cookies
        self.Dict["custom_headers"] = custom_headers
        
    def Process(self,BotData):


        local_url = ReplaceValues(self.url,BotData)
        request = OBRequest()
        request.Setup(self.auto_redirect)

        if self.request_type == RequestType.Standard:
            request.SetStandardContent(ReplaceValues(self.post_data, BotData), ReplaceValues(self.ContentType, BotData), self.method, self.encode_content)
        elif self.request_type == RequestType.BasicAuth:
            request.SetBasicAuth(ReplaceValues(self.auth_user,BotData), ReplaceValues(self.auth_pass,BotData))

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
            (Address, ResponseCode, ResponseHeaders, ResponseCookies) = request.Perform(self.url, self.method)
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
                