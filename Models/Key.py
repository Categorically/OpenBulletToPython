from Functions.Conditions.Condition import ReplaceAndVerify


class Key:
    def __init__(self,LeftTerm="",Comparer="",RightTerm=""):
        self.LeftTerm = LeftTerm
        self.Comparer = Comparer
        self.RightTerm = RightTerm

    def CheckKey(self):
        try:
            return ReplaceAndVerify(self.LeftTerm,self.Comparer,self.RightTerm)
        except:
            # Return false if e.g. we can't parse the number for a LessThan/GreaterThan comparison. 
            return False
        