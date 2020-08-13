import re

def LR(input_string, left, right,recursive=False,useRegex=False):
    if not left and not right:
        return [input_string]

    if not left and left in input_string or not right and right in input_string:
        return [input_string]
    
    partial = input_string
    pFrom = 0
    pFrom = 0 
    List = []


    if recursive:
        if useRegex:
            pattern = re.compile(BuildLRPattern(left,right))
            mc = re.findall(pattern,input_string)
            for m in mc:
                List.append(m)
        else:
            while left in partial and right in partial:
                pFrom = (int(partial.find(left)) + int(len(str(left))))
                partial = partial[pFrom:]
                pTo = int(partial.find(right))
                parsed = partial[0:int(pTo)]

                List.append(parsed)
                partial = partial[len(parsed) + len(right):]
                
    else:
        if useRegex:
            pattern = re.compile(BuildLRPattern(left,right))
            mc = re.findall(pattern,input_string)
            if len(mc) > 0: List.append(mc[0])
        else:
            pFrom = (int(partial.find(left)) + int(len(str(left))))
            partial = partial[pFrom:]
            pTo = int(partial.find(right))
            parsed = partial[0:int(pTo)]
            List.append(parsed)
    return List

def JSON(input_string:str,field:str,recursive:bool,useJToken:bool):
    import json
    import jsonpath_ng
    from jsonpath_ng import jsonpath
    from jsonpath_ng import parse as JTParse
    listArray = []
    if useJToken:

        if recursive:

            jsonpath_expr = JTParse(field)
            jsonList = [match.value for match in jsonpath_expr.find(json.loads(input_string))]
            for j in jsonList:
                listArray.append(str(j))
        else:
            jsonList = json.loads(input_string)
            try:
                listArray.append(str(jsonList[field]))
            except:
                listArray.append("")
    else:
        jsonList = json.loads(input_string)
        for key,value in jsonList.items():
            if key == field:
                listArray.append(value)
        if not recursive and len(listArray) > 1: listArray = [listArray[0]]
    return listArray
    
def BuildLRPattern(ls,rs):
    left = ls
    right = rs
    if not ls: left = "^"
    if not rs: right = "$"

    return "(?<=" + left + ").+?(?=" + right + ")"