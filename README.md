# OpenBulletToPython
OpenBulletToPython using code from OpenBullet

This is not a user enumeration tool. The name is borrowed from OpenBullet but will not have support for wordlists, wordlist types.

# Parsing Loliscript
- [x] PARSE
- [x] REQUEST
- [x] KEYCHECK
- [x] FUNCTIONS
- [x] UTILITY

# Processing Blocks
- FUNCTION
  - [x] Constant
  - [x] Base64Encode
  - [x] Base64Decode
  - [x] ToUppercase
  - [x] ToLowercase
  - [x] Length
  - [x] Replace
  - [x] URLEncode
  - [x] URLDecode
  - [x] Hash
  - [x] HMAC
  - [x] RandomNum
  - [x] RandomString
  - [x] CurrentUnixTime
  - [x] UnixTimeToDate
    - [ ] Dynamic DateFormat
  - [x] Ceil
  - [x] Floor
  - [x] Round
  - [ ] Compute
  - [x] CountOccurrences
  - [x] CharAt
  - [x] Substring
  - [x] ReverseString
  - [x] Trim
  - [x] GetRandomUA
  - [x] PBKDF2PKCS5
  - [x] UnixTimeToISO8601
  - [x] Unescape
  - [x] ClearCookies
  - [x] HTMLEntityEncode
  - [x] HTMLEntityDecode

- REQUEST
  - [x] Standard
  - [x] BasicAuth
  - [x] Multipart
  - [x] Raw

- PARSE
  - [x] LR
  - [x] CSS
  - [x] JSON
  - [x] REGEX
    - [ ] EncodeOutput
    - [ ] DotMatches

- KEYCHECK
  - [ ] CUSTOM

- UTILITY
  - [x] List
  - [x] Variable
  - [x] Conversion
  - [x] File
  - [x] Folder
  
 
```Python
from OpenBullet import OpenBullet

config_text = r"""REQUEST GET "https://google.com" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" 

KEYCHECK 
  KEYCHAIN Success OR 
    KEY "title>Google" """

username = "username"
password = "password"

open_bullet = OpenBullet(config=config_text, USER=username, PASS=password)
print(open_bullet.run())
```
```
>>> GET https://google.com
>>> SUCCESS
```
 https://github.com/openbullet/openbullet
