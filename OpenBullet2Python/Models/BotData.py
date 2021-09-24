from OpenBullet2Python.Models.VariableList import VariableList

from enum import Enum


class BotData:
    class BotStatus(str,Enum):
        NONE = "NONE"
        ERROR = "ERROR"
        SUCCESS = "SUCCESS"
        FAIL = "FAIL"
        BAN = "BAN"
        RETRY = "RETRY"
        CUSTOM = "CUSTOM"
    def __init__(self,status=BotStatus.NONE):
        self.Variables = VariableList()
        self.status = status
        self.cwd = None

    def ResponseSourceGet(self):
        return self.Variables.GetWithName("SOURCE").Value
    def ResponseSourceSet(self,variable):
        self.Variables.Set(variable)

    def AddressGet(self):
        return self.Variables.GetWithName("ADDRESS").Value
    def AddressSet(self,variable):
        self.Variables.Set(variable)

    def ResponseCodeGet(self):
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
