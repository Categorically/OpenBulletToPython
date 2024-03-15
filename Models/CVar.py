

class VarType:
    Single = "Single"
    List = "List"
    Dictionary = "Dictionary"
class CVar:
    """
    Name: str
    Value: [str, list, dict]
    IsCapture: bool
    Hidde: bool
    """

    def __init__(self, Name:str, Value,IsCapture:bool=False,Hidden=False):

        if type(Value) == list:
            self.var_type = VarType.List
        elif type(Value) == str:
            self.var_type = VarType.Single
        elif type(Value) == dict:
            self.var_type = VarType.Dictionary

        self.Name = Name
        self.Value = Value
        self.IsCapture = IsCapture
        self.Hidden = Hidden
    def __repr__(self) -> str:
        return f"CVar(Name={self.Name}, Value={self.Value}, IsCapture={self.IsCapture}, Hidden={self.Hidden})"
    def ToString(self):
        if self.var_type == VarType.Single:
            return self.Value
        elif self.var_type == VarType.List:
            if type(self.Value == list): return "[" + ",".join(self.Value) + "]"
            else: return ""
        elif self.var_type == VarType.Dictionary:
            return "{" + ",".join(["(" + v[0] + ", " + v[1] + ")" for v in self.Value.items()]) + "}"
    
    def GetListItem(self,index):
        if self.var_type != VarType.List: return None

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