from OpenBullet2Python.LoliScript.Loliscript import CompressedLines
from OpenBullet2Python.LoliScript.BlockParser import Parse
from OpenBullet2Python.Models.BotData import BotData
from OpenBullet2Python.Models.CVar import CVar
import os

class OpenBullet:
    def __init__(self,config:str, data:BotData = None, USER:str = None, PASS:str = None, output_path:str = None) -> None:

        self.blocks = []
        self.config = config
        if not data:
            self.data = BotData()
        else:
            self.data = data
        
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