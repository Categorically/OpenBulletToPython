

class VarType:
    def __init__(self):
        self.Single = "Single"
        self.List = "List"
        self.Dictionary = "Dictionary"
class CVar:

    def __init__(self, Name, Value,IsCapture,Hidden=False):
        # Not sure how this is done in c#

        if type(Value) == list:
            self.VarType = VarType().List
        elif type(Value) == str:
            self.VarType = VarType().Single
        elif type(Value) == dict:
            self.VarType = VarType().Dictionary

        self.Name = Name
        self.Value = Value
        self.IsCapture = IsCapture
        self.Hidden = Hidden
    
    def ToString(self):
        if self.VarType == VarType().Single:
            return self.Value
        elif self.VarType == VarType().List:
            if type(self.Value == list): return "[" + ",".join(self.Value) + "]"
            else: return ""
        elif self.VarType == VarType().Dictionary:
            return "{" + ",".join(["(" + v[0] + ", " + v[1] + ")" for v in self.Value.items()]) + "}"
    
    def GetListItem(self,index):
        if self.VarType != VarType().List: return None

        List = list(self.Value)

        if index < 0:
            index = len(List) + index    
        
        if index > len(List) - 1 or index < 0: return None
        return List[index]

    def GetDictValue(self,key):
        Dict = self.Value
        Dict = next((v for v in self.Value.items() if v[0] == key),None)
        if Dict:
            return Dict[1]
        else:
            print("Key not in dictionary")
            return None

    def GetDictKey(self,value):
        Dict = self.Value
        Dict = next((v for v in self.Value.items() if v[1] == value),None)
        if Dict:
            return Dict[0]
        else:
            print("Value not in dictionary")
            return None