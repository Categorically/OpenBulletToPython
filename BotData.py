from VariableList import VariableList

class BotData:
    Variables = VariableList()
    class ResponseSource():
        def get(self):
            BotData().Variables.GetWithName("SOURCE").Value
        def set(self,variable):
            BotData().Variables.Set(variable)

    class Address():
        def get(self):
            BotData().Variables.GetWithName("ADDRESS").Value
        def set(self,variable):
            BotData().Variables.Set(variable)

    class ResponseCode():
        def get(self):
            BotData().Variables.GetWithName("RESPONSECODE").Value
        def set(self,variable):
            BotData().Variables.Set(variable)

    class ResponseHeaders():
        def get(self):
            BotData().Variables.GetWithName("HEADERS").Value
        def set(self,variable):
            BotData().Variables.Set(variable)

    class Cookies():
        def get(self):
            BotData().Variables.GetWithName("COOKIES").Value
        def set(self,variable):
            BotData().Variables.Set(variable)
