from Functions.Conditions.Condition import ReplaceAndVerify


class Key:
    def __init__(self,LeftTerm="",Comparer="",RightTerm=""):
        self.LeftTerm = LeftTerm
        self.Comparer = Comparer
        self.RightTerm = RightTerm

    def CheckKey(self,BotData):
        try:
            return ReplaceAndVerify(self.LeftTerm,self.Comparer,self.RightTerm,BotData)
        except Exception:
            # Return false if e.g. we can't parse the number for a LessThan/GreaterThan comparison. 
            return False
        