import re
import json
import jsonpath_ng
from jsonpath_ng import jsonpath
from jsonpath_ng import parse as JTParse

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
            except Exception:
                listArray.append("")
    else:
        jsonlist = []
        dictList = parseJSON("", input_string, jsonlist)
        for j in dictList:
            if j.get(field) != None:
                value = j.get(field)
                # The substring is a hack to remove the " from the string dump
                if value.startswith('"'):
                    listArray.append(value[1:len(value) - 1])
                else:
                    listArray.append(value)

        if not recursive and len(listArray) > 1: listArray = [listArray[0]]
    return listArray

def parseJSON(a,b,jsonlist:list):
    jsonlist.append({a:b})

    if b.startswith("["):
        array = []
        try:
            array = json.loads(b)
        except Exception:
            return
        for x in array:
            parseJSON("",json.dumps(x),jsonlist)
    elif b.startswith("{"):
        obj = None
        try:
            obj = json.loads(b)
        except Exception:
            return
        for key,value in obj.items():
            parseJSON(key,json.dumps(value),jsonlist)
    return jsonlist

def REGEX(inputString:str, pattern:str, output:str, recursive=False):
    List = []
    if recursive:
        r = re.compile(pattern)
        mers = r.finditer(inputString)
        for m in mers:
            final = output
            i = 0
            while 1:
                try:
                    final = final.replace("[" + str(i) + "]", str(m[i]))
                except Exception:
                    break
                i += 1
            List.append(final)
    else:
        r = re.compile(pattern)
        m = r.search(inputString)
        final = output
        i = 0
        while 1:
            try:
                final = final.replace("[" + str(i) + "]", str(m[i]))
            except Exception:
                break
            i += 1
        List.append(final)

    return List

def BuildLRPattern(ls,rs):
    left = ls
    right = rs
    if not ls: left = "^"
    if not rs: right = "$"

    return "(?<=" + left + ").+?(?=" + right + ")"