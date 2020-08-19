from OpenBullet2Python.Models.CVar import CVar
from OpenBullet2Python.Models.CVar import VarType
class VariableList:

    # All = [CVar("SOURCE","SOURCE",True,False)]
    All = []
    # Captures = [v for v in All if v.IsCapture == True and v.Hidden == False]
    def Captures(self):
        return [v for v in self.All if v.IsCapture == True and v.Hidden == False]
    Singles = [v for v in All if v.VarType == VarType().Single]
    Lists = [v for v in All if v.VarType == VarType().List]
    Dictionaries = [v for v in All if v.VarType == VarType().Dictionary]

    def VariableList(self):
        self.All = []

    def VariableListWithList(self,List):
        self.All = List

    # Renamed from Get
    def GetWithName(self,name):
        return next((v for v in self.All if v.Name == name),None)

    # Renamed from Get
    def GetWithNameAndType(self,name,VarType):
        return next((v for v in self.All if v.VarType == VarType and v.Name == name),None)
        
    def GetSingle(self,name):
        return self.GetWithNameAndType(name,VarType().Single).Value
    
    def GetList(self,name):
        return self.GetWithNameAndType(name,VarType().List).Value

    def GetDictionary(self,name):
        return self.GetWithNameAndType(name,VarType().Dictionary)

    def VariableExists(self,name):
        return any([v for v in self.All if v.Name == name])

    # Renamed from VariableExists
    def VariableExistsWithType(self,name, VarType):
        return any([v for v in self.All if v.Name == name and v.VarType == VarType])
    
    def Set(self,variable:CVar):
        self.Remove(variable.Name)

        self.All.append(variable)
    def SetNew(self, variable):
        if self.VariableExists(variable.Name) == False: self.Set(variable)
    def Remove(self,name):
        self.All = [v for v in self.All if v.Name != name]

    def ToCaptureString(self):
        return " | ".join([v.Name + "=" + v.ToString() for v in self.Captures()]) 