from OpenBullet import OpenBullet

configs = []

google_example_config = r"""REQUEST GET "https://google.com" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" 

KEYCHECK 
  KEYCHAIN Success OR 
    KEY "title>Google" """

bing_example_config = r"""REQUEST GET "https://www.bing.com" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" 

KEYCHECK 
  KEYCHAIN Success OR 
    KEY "title>Bing" """

configs.append(google_example_config)
configs.append(bing_example_config)

username = "username"
password = "password"

for config in configs:
  open_bullet = OpenBullet(config=config, USER=username, PASS=password)
  print(open_bullet.run())