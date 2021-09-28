from requests import Request, Session
from requests.auth import HTTPBasicAuth
from requests.utils import quote
from OpenBullet2Python.Functions.Conversion.Conversion import Conversion, EncodingType
from enum import Enum
import random
from math import floor

class MultipartContentType(str, Enum):
    String = "String"
    File = "File"


class MultipartContent:
    def __init__(self, Name:str, Value:str, Type:MultipartContentType, ContentType:str = "") -> None:
        self.Name = Name
        self.Value = Value
        self.Type = Type
        self.ContentType = ContentType
class OBRequest():
    def __init__(self) -> None:
        pass
    
    def Setup(self, auto_redirect:bool, timeout:int=30):
        self.session = Session()
        self.request = Request()
        self.timeout = timeout # Seconds
        self.auto_redirect = auto_redirect

    def SetStandardContent(self, postData:str, contentType:str, Method:str, encodeContent:bool = False):
        if encodeContent:
            postData = quote(postData, "=&")
        if contentType:
            self.request.headers["Content-Type"] = contentType
            self.request.data = postData

        return

    def SetRawContent(self, rawData:str, contentType:str):
        if contentType:
            self.request.headers["Content-Type"] = contentType
            rData = Conversion().ConvertFrom(rawData,EncodingType.HEX)
            self.request.data = rData

    def SetBasicAuth(self, user:str, password:str):
        self.request.auth = HTTPBasicAuth(user, password)

    def SetMultipartContent(self, contents:list[MultipartContent], boundary:str):
        self.request.files = []
        bdry = boundary or GenerateMultipartBoundary()
        self.request.headers["Content-Type"] = f"multipart/form-data; boundary={bdry}"
        for c in contents:
            if c.Type == MultipartContentType.String:
                self.request.files.append((c.Name, (c.Value)))
            elif c.Type == MultipartContentType.File:
                self.request.files.append((c.Name, open(c.Value, "rb")))
        
    def Perform(self, url, method):
        self.request.url = url
        self.request.method = method
        request = self.session.prepare_request(self.request)
        self.response = self.session.send(request, timeout=self.timeout, allow_redirects=self.auto_redirect)


        address = self.response.url
        responseCode = str(self.response.status_code)
        headers = dict(self.response.headers)
        cookies = dict(self.response.cookies)


        return (address, responseCode, headers, cookies)

    def SaveString(self, readResponseSource:bool, headers:dict):
        return self.response.text
    
    def SetHeaders(self, headers:dict, acceptEncoding:bool = False):
        for h in headers.items():
            replacedKey = h[0].replace("-","").lower()
            if replacedKey == "acceptencoding": # Brotli not supported
                headers["Accept"] = "*"
            elif replacedKey == "contenttype": # Already set
                pass
            else:
                self.request.headers[h[0]] = h[1]

    def SetCookies(self, cookies:dict):
        self.request.cookies = cookies

def GenerateMultipartBoundary():
    string = ""
    for x in range(16):
        ch = chr(int(floor(26 * random.random() + 65)))
        string += ch.lower()
    return f"------WebKitFormBoundary{string}"