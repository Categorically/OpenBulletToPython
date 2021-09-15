from enum import Enum
import re
from OpenBullet2Python.Blocks.BlockBase import ReplaceValuesRecursive,ReplaceValues
class Comparer(Enum):
    LessThan = "LessThan"
    GreaterThan = "GreaterThan"
    EqualTo = "EqualTo"
    NotEqualTo = "NotEqualTo"
    Contains = "Contains"
    DoesNotContain = "DoesNotContain"
    Exists = "Exists"
    DoesNotExist = "DoesNotExist"
    MatchesRegex = "MatchesRegex"
    DoesNotMatchRegex = "DoesNotMatchRegex"


def ReplaceAndVerify(Left,comparer,Right,BotData):
    L = ReplaceValuesRecursive(Left,BotData)
    R = ReplaceValues(Right,BotData)

    if comparer == Comparer.EqualTo:
        return any([l for l in L if l == R])
    elif comparer == Comparer.EqualTo:
        return any([l for l in L if l != R])
    elif comparer == Comparer.GreaterThan:
        return any([l for l in L if float(l.replace(",",".")) > float(R.replace(",","."))])
    elif comparer == Comparer.LessThan.value:
        return any([l for l in L if float(l.replace(",",".")) < float(R.replace(",","."))])
    elif comparer == Comparer.Contains:
        return any([l for l in L if R in l])
    elif comparer == Comparer.DoesNotContain:
        return any([l for l in L if R not in l])
    elif comparer == Comparer.Exists.value:
        return any([l for l in L if l != Left])
    elif comparer == Comparer.DoesNotExist:
        return any([l for l in L if l == Left])
    elif comparer == Comparer.MatchesRegex:
        return any([l for l in L if re.match(l,R)])
    elif comparer == Comparer.DoesNotMatchRegex:
        return any([l for l in L if not re.match(l,R)])
    else:
        # Todo
        pass
