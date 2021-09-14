from OpenBullet2Python.Models.BotData import BotData
from OpenBullet2Python.TestConfig import TestConfig
from OpenBullet2Python.Models.CVar import CVar

# This holds the variable list.
data = BotData()

# By default Status is set to BotStatus.NONE
print(data.status.value)

# Make sure it is a raw string or python will encode \" as "
config_text = r"""REQUEST GET "https://google.com" 
  
  HEADER "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36" 
  HEADER "Pragma: no-cache" 
  HEADER "Accept: */*" 

KEYCHECK 
  KEYCHAIN Success OR 
    KEY "title>Google" """

# Adding a variable for replacement
# This will add a variable called "USER" with the value as "username", ect
data.Variables.Set(CVar("USER","username",False,True))
data.Variables.Set(CVar("PASS","password",False,True))

for variable in data.Variables.all:
    print(f"Name: {variable.Name}, Value: {variable.Value}" )


# Run the config
# If the the status changes to Fail, Ban or an Error then it will return, else it runs until all the blocks are processed.
# There is no error handling so be careful on what you run.
TestConfig(config_text,data)


# The outcome of the config test
print(data.Status.value)