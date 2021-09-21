import re
from OpenBullet2Python.Models.BotData import BotData
from OpenBullet2Python.Models.CVar import VarType
from OpenBullet2Python.Models.CVar import CVar
def ParseArguments(input_string, delimL, delimR):
    output = []
    pattern = "\\" + delimL + "([^\\" + delimR + "]*)\\" + delimR
    matches = re.findall(pattern, input_string)
    for match in matches:
        output.append(match)
    return output

def ReplaceValues(input_string,BotData):
    if input_string == None: return input_string
    if "<" not in input_string and ">" not in input_string: return input_string

    previous = ""
    output = input_string
    args = None
    while "<" in output and ">" in output and output != previous:
        previous = output
        r = re.compile('<([^<>]*)>')
        full = ""
        m = ""
        matches = r.findall(output)

        for match in matches:

            full = "<" + match + ">"

            m = match

            r = re.compile('^[^\\[\\{\\(]*')
            name = r.search(m).group(0)
            

            v = BotData.Variables.GetWithName(name)

            if not v: return output

            args = m.replace(name,"")
            
            if v.var_type == VarType.Single:
                output = output.replace(full, v.Value)

            elif v.var_type == VarType.List:
                # If it's just the list name, replace it with its string representation
                if not args: 
                    output = output.replace(full,v.ToString())

                elif "[" in args and "]" in args:
                    index = 0
                    try:
                        index = int(ParseArguments(args, "[", "]")[0])
                        item = v.GetListItem(index)
                        if item:
                            output = output.replace(full,item)
                    except Exception:
                        pass

            elif v.var_type == VarType.Dictionary:

                if "(" in args and ")" in args:
                    dicKey = ParseArguments(args, "(", ")")[0]
                    output = output.replace(full, v.GetDictValue(dicKey))

                elif "{" in args and "}" in args:
                    dicVal = ParseArguments(args, "{", "}")[0]
                    output = output.replace(full, v.GetDictKey(dicVal))

                # If it's just the dictionary name, replace it with its string representation
                else: 
                    output = output.replace(full,v.ToString())
        
    return output


def ReplaceValuesRecursive(input_string,BotData):


    toReplace = []
    r = re.compile('<([^\\[]*)\\[\\*\\]>')
    matches = r.findall(input_string)

    variables = []


    for m in matches:
        name = m

        variable = BotData.Variables.GetWithName(name)
        if variable:
            if variable.var_type == VarType.List: variables.append(variable)
        
            
    def theEnd(toReplace,BotData):
        toReplace = [ReplaceValues(replace,BotData) for replace in toReplace]
        return toReplace

    if len(variables) > 0:
        max_index = len(variable.Value)
        i = 0

        while i < max_index:
            replaced = input_string

            for variable in variables:
                variable_Name = variable.Name
                theList = variable.Value
                if len(theList) > i:
                    replaced = replaced.replace(f"<{variable_Name}[*]>", str(theList[i]))
                else:
                    replaced = replaced.replace(f"<{variable_Name}[*]>", "NULL")

            toReplace.append(replaced)
            i += 1
        return theEnd(toReplace,BotData)


    r = re.compile("<([^\\(]*)\\(\\*\\)>")
    match = r.match(input_string)

    if match:
        full = match.group(0)
        name = match.group(1)

        theDict = BotData.Variables.GetDictionary(name)

        if not theDict: toReplace.append(input_string)
        else:
            theDict = theDict.Value
            for key in theDict:
                aDict = {key,theDict[key]}
                toReplace.append(input_string.replace(full,str(aDict)))
        return theEnd(toReplace,BotData)
    
    r = re.compile("<([^\\{]*)\\{\\*\\}>")
    match = r.match(input_string)

    if match:
        full = match.group(0)
        name = match.group(1)

        theDict = BotData.Variables.GetWithName(name)

        if not theDict: toReplace.append(input_string)
        else:
            theDict = theDict.Value
            for key in theDict:
                toReplace.append(input_string.replace(full,str(key)))
        return theEnd(toReplace,BotData)
    toReplace.append(input_string)
    return theEnd(toReplace,BotData)

def InsertVariable(BotData,isCapture,recursive,values,variableName,prefix="" ,suffix="" ,urlEncode=False ,createEmpty=True):
    # thisList = [ReplaceValues(prefix, bot_data) + str(v).strip() + ReplaceValues(suffix,bot_data) for v in values]
    thisList = values
    if urlEncode == False: pass

    variable = None

    if recursive:
        if len(thisList) == 0:
            if createEmpty:
                variable = CVar(variableName,thisList,isCapture)
        else:
            variable = CVar(variableName,thisList,isCapture)
    else:
        if len(thisList) == 0:
            if createEmpty:
                variable = CVar(variableName,"",isCapture)
        else:
            variable = CVar(variableName,thisList[0],isCapture)
    if variable:
        BotData.Variables.Set(variable)
    return True