from requests import Request, Session
from requests.api import request
from requests.auth import HTTPBasicAuth
from requests.utils import quote
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

    def SetRawContent(self):
        pass

    def SetBasicAuth(self, user:str, password:str):
        self.request.auth = HTTPBasicAuth(user, password)

    def SetMultipartContent(self):
        pass
    
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