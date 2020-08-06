# OpenBullet2Python
OpenBullet2Python using code from OpenBullet

#Parsing Loliscript into dicts
- [x] PARSE
- [x] REQUEST
- [x] KEYCHECK
- [x] FUNCTIONS

```
from ToPython import ToPython
config_text = """REQUEST GET "https://google.com" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" """
  
blocks = ToPython(config_text)

>>> [{'Method': 'GET', 'Url': 'https://google.com', 'Booleans': {}, 'CustomCookies': {}, 'CustomHeaders': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Pragma': 'no-cache', 'Accept': '*/*'}, 'label': '', 'block_type': 'REQUEST'}]
```
Using Parse to init the block is only temp
```
from BotData import BotData
from BlockParser import Parse
data = BotData()
config_text = """FUNCTION Constant "test123" -> VAR "test" 
FUNCTION Constant "<test>" -> VAR "testagain" """
compressed = CompressedLines(config_text)
for c in compressed:
  block = Parse(c)
  block.Process()

>>> Executed function Constant on input ['test123'] with outcome test123
>>> Executed function Constant on input ['test123'] with outcome test123
 ```
