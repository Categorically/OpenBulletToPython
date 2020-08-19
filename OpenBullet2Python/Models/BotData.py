from OpenBullet2Python.Models.VariableList import VariableList

from enum import Enum


class BotData:
    class BotStatus(Enum):
        NONE = "NONE"
        ERROR = "ERROR"
        SUCCESS = "SUCCESS"
        FAIL = "FAIL"
        BAN = "BAN"
        RETRY = "RETRY"
        CUSTOM = "CUSTOM"

    Variables = VariableList()
    Status = BotStatus.NONE

    class ResponseSource():
        def get(self):
            return BotData.Variables.GetWithName("SOURCE").Value
        def set(self,variable):
            BotData.Variables.Set(variable)

    class Address():
        def get(self):
            return BotData.Variables.GetWithName("ADDRESS").Value
        def set(self,variable):
            BotData.Variables.Set(variable)

    class ResponseCode():
        def get(self):
            return BotData.Variables.GetWithName("RESPONSECODE").Value
        def set(self,variable):
            BotData.Variables.Set(variable)

    class ResponseHeaders():
        def get(self):
            return BotData.Variables.GetWithName("HEADERS").Value
        def set(self,variable):
            BotData.Variables.Set(variable)

    class Cookies():
        def get(self):
            return BotData.Variables.GetWithName("COOKIES")
        def set(self,variable):
            BotData.Variables.Set(variable)
