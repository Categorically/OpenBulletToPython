from OpenBullet2Python.Models.VariableList import VariableList

from enum import Enum


class BotData:
    def __init__(self):
        self.Variables = VariableList()
    class BotStatus(Enum):
        NONE = "NONE"
        ERROR = "ERROR"
        SUCCESS = "SUCCESS"
        FAIL = "FAIL"
        BAN = "BAN"
        RETRY = "RETRY"
        CUSTOM = "CUSTOM"
        
    Status = BotStatus.NONE

    def ResponseSource(self):
        def get(self):
            return self.Variables.GetWithName("SOURCE").Value
    def ResponseSourceSet(self,variable):
        self.Variables.Set(variable)

    def Address(self):
        def get(self):
            return self.Variables.GetWithName("ADDRESS").Value
    def AddressSet(self,variable):
        self.Variables.Set(variable)

    def ResponseCode(self):
        def get(self):
            return self.Variables.GetWithName("RESPONSECODE").Value
    def ResponseCodeSet(self,variable):
        self.Variables.Set(variable)

    def ResponseHeadersGet(self):
        return self.Variables.GetWithName("HEADERS").Value
    def ResponseHeadersSet(self,variable):
        self.Variables.Set(variable)

    def CookiesGet(self):
        return self.Variables.GetWithName("COOKIES")
    def CookiesSet(self,variable):
        self.Variables.Set(variable)
