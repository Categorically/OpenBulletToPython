from OpenBullet2Python.Models.BotData import BotData
from OpenBullet2Python.auxiliary_functions import process_blocks
from OpenBullet2Python.Models.CVar import CVar

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

for config in configs:
    # Init the data class for each config. The class stores the outcome and the variables created during runtime.
    data = BotData()

    # Create a new CVar object with name and value
    user_variable = CVar("USER","username",False,True)
    # Add the object to the variables
    data.Variables.Set(user_variable)

    password_variable = CVar("PASS","password",False,True)
    data.Variables.Set(password_variable)

    # Run each block until the config reaches the outcome
    process_blocks(config,data)
    # The outcome of the config
    print(data.status.value)