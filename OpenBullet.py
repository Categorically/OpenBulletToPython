from OpenBullet2Python.auxiliary_functions import process_blocks
from OpenBullet2Python.Models.BotData import BotData
from OpenBullet2Python.Models.CVar import CVar

class OpenBullet:
    def __init__(self,config:str, data:BotData = None, USER:str = None, PASS:str = None) -> None:

        self.config = config
        if not data:
            self.data = BotData()
        else:
            self.data = data
        
        if USER:
            data.Variables.Set(CVar("USER",USER,False,True))
        if PASS:
            data.Variables.Set(CVar("PASS",PASS,False,True))

        

    def start(self):
        process_blocks(self.config, self.data)
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
    open_bullet.start()
    print(open_bullet.status())
