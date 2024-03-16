from Models.CVar import CVar
from Models.CVar import VarType

from Functions.Conditions.Condition import Comparer, ReplaceAndVerify
class VariableList:
    def __init__(self):
        self.all:list[CVar] = []
    # Captures = [v for v in all if v.IsCapture == True and v.Hidden == False]
    def Captures(self):
        return [v for v in self.all if v.IsCapture == True and v.Hidden == False]

    def VariableList(self):
        self.all = []

    def VariableListWithList(self,List):
        self.all = List

    # Renamed from Get
    def GetWithName(self,name):
        return next((v for v in self.all if v.Name == name),None)

    # Renamed from Get
    def GetWithNameAndType(self,name,var_type):
        return next((v for v in self.all if v.var_type == var_type and v.Name == name),None)
        
    def GetSingle(self,name):
        return self.GetWithNameAndType(name,VarType.Single).Value
    
    def GetList(self,name):
        # return self.GetWithNameAndType(name,VarType.List).Value
        v = self.GetWithNameAndType(name,VarType.List)
        if v:
            return v.Value
        else:
            return None
        


    def GetDictionary(self,name):
        return self.GetWithNameAndType(name,VarType.Dictionary)

    def VariableExists(self,name):
        return any([v for v in self.all if v.Name == name])

    # Renamed from VariableExists
    def VariableExistsWithType(self,name, var_type):
        return any([v for v in self.all if v.Name == name and v.var_type == var_type])
    
    def Set(self,variable:CVar):
        self.Remove(variable.Name)

        self.all.append(variable)
    def SetNew(self, variable):
        if self.VariableExists(variable.Name) == False: self.Set(variable)
    def Remove(self,name):
        self.all = [v for v in self.all if v.Name != name]

    def RemoveWithComparer(self, comparer:Comparer, name:str, data):
        self.all = [v for v in self.all if v.Hidden and not ReplaceAndVerify(v.Name, comparer, name, data)]

    def ToCaptureString(self):
        return " | ".join([v.Name + "=" + v.ToString() for v in self.Captures()]) 