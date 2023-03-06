from LoliScript.Loliscript import CompressedLines
from LoliScript.BlockParser import Parse
from Models.BotData import BotData, proxyType
from Models.CVar import CVar
from typing import Union
import os

class OpenBullet:
    def to_request_proxy(proxy:str, proxy_type:proxyType) -> Union[dict, None]:
        ip = None
        port = None
        username = None
        password = None

        try:
            if proxy.count(":") == 1: # "ip:port"
                ip, port = proxy.split(":", 1)
            elif proxy.count(":") == 3: # "username:password:ip:port"
                username, password, ip, port = proxy.split(":", 3)
            
        except Exception:
            return None
        proxy_uri = None
        if username and password:
            proxy_uri = username + ":" + password + "@" + ip + ":" + port
        else:
            proxy_uri = ip + ":" + port

        request_proxy = {}
        if proxy_type == proxyType.HTTP or proxy_type == proxyType.HTTPS:
            request_proxy["http"] = "http://" + proxy_uri

        if proxy_type == proxyType.HTTP:
            request_proxy["https"] = "http://" + proxy_uri
        elif proxy_type == proxyType.HTTPS:
            request_proxy["https"] = "https://" + proxy_uri

        if proxy_type == proxyType.SOCKS4:
            request_proxy["http"] = "socks4://" + proxy_uri
            request_proxy["https"] = "socks4://" + proxy_uri
        elif proxy_type == proxyType.SOCKS5:
            request_proxy["http"] = "socks5://" + proxy_uri
            request_proxy["https"] = "socks5://" + proxy_uri
        return request_proxy
    def __init__(self,config:str, data:BotData = None, USER:str = None, PASS:str = None, output_path:str = None,
                proxy:Union[str, None] = None, proxy_type:Union[str, proxyType] = proxyType.HTTP) -> None:
        """Proxy format: 
        Username:Password:Ip:Port"""
        self.blocks = []
        self.config = config
        if not data:
            self.data = BotData()
        else:
            self.data = data
        
        if proxy:
            request_proxy = self.to_request_proxy(proxy, proxy_type)
            self.data.proxy = request_proxy

        if USER:
            self.data.Variables.Set(CVar("USER",USER,False,True))
        if PASS:
            self.data.Variables.Set(CVar("PASS",PASS,False,True))
        
        # Current working dir
        if output_path:
            self.data.cwd = output_path
        else:
            self.data.cwd = os.getcwd()

    def parse(self):
        compressed = CompressedLines(self.config)
        for c in compressed:
            try:
                block = Parse(c)
            except Exception as e:
                print(e)
                return
            if block: self.blocks.append(block)

    def process(self):
        for block in self.blocks:
            if self.data.status.value == self.data.BotStatus.FAIL or self.data.status.value == self.data.BotStatus.BAN or self.data.status.value == self.data.BotStatus.ERROR:
                return
            try:
                block.Process(self.data)
            except Exception as e:
                print(e)
                return 
                
    def run(self):
        self.parse()
        if self.blocks:
            self.process()
            return self.status()
        else:
            print("No blocks to process")
    def status(self):
        return self.data.status.value
        
    
if __name__ == "__main__":
    config_text = r"""REQUEST GET "https://google.com" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" 

KEYCHECK 
  KEYCHAIN Success OR 
    KEY "title>Google" """

    open_bullet = OpenBullet(config=config_text)
    print(open_bullet.run())