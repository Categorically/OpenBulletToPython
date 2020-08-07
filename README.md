# OpenBullet2Python
OpenBullet2Python using code from OpenBullet

# Parsing Loliscript
- [x] PARSE
- [x] REQUEST
- [x] KEYCHECK
- [x] FUNCTIONS


```Python
from ToPython import ToPython
config_text = """REQUEST GET "https://google.com" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" """
  
blocks = ToPython(config_text)
```

```
>>> [{'Method': 'GET', 'Url': 'https://google.com', 'Booleans': {}, 'CustomCookies': {}, 'CustomHeaders': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36', 'Pragma': 'no-cache', 'Accept': '*/*'}, 'label': '', 'block_type': 'REQUEST'}]
```

# Processing Blocks
- FUNCTION
  - [x] Constant
- REQUEST
  - [ ] Standard
    - [x] GET
    - [x] POST
    - [ ] PUT
    - [ ] OPTIONS
  - [ ] BasicAuth
  - [ ] Multipart
  - [ ] Raw
- PARSE
  - [x] LR
    - [x] UseRegexLR
  - [ ] CSS
  - [ ] JSON
  - [ ] REGEX
- KEYCHECK
  - [ ] CUSTOM 
  
```Python
# Temp
from BotData import BotData
from BlockParser import Parse
data = BotData()
# Make sure it is a raw string or python will encode \" as "
config_text = r"""FUNCTION Constant "test123" -> VAR "test" 
FUNCTION Constant "<test>" -> VAR "testagain" 
PARSE "test" LR "t" "t" -> VAR "NewVar
"""
compressed = CompressedLines(config_text)
for c in compressed:
  block = Parse(c)
  block.Process()
```
```
>>> Executed function Constant on input ['test123'] with outcome test123
>>> Executed function Constant on input ['test123'] with outcome test123
>>> Parsed ['es'] From test
 ```
 
```Python
#Temp
from BotData import BotData
from BlockParser import Parse
data = BotData()
print(data.Status.value)
# Make sure it is a raw string or python will encode \" as "
config_text = r"""KEYCHECK 
  KEYCHAIN Success OR 
    KEY "test" Contains "test""""
compressed = CompressedLines(config_text)
for c in compressed:
  block = Parse(c)
  if block:
    block.Process()
    print(data.Status.value)
```
```
>>> NONE
>>> SUCCESS
```
 https://github.com/openbullet/openbullet
