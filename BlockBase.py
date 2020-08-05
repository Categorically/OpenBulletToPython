import re
def ParseArguments(input_string, delimL, delimR):
    output = []
    pattern = "\\" + delimL + "([^\\" + delimR + "]*)\\" + delimR
    matches = re.findall(pattern, input_string)
    for match in matches:
        output.append(match)
    return output

def ReplaceValues(input_string, bot_data):
    """ Example: bot_data = {"Variables": {"SOURCE":{"Value": ["wadaw"],
                                                     "Type": "List",
                                                     "Name": "SOURCE"}},
                             "GlobalVariables": {}}"""

    if "<" not in input_string and ">" not in input_string: return input_string

    previous = ""
    output = input_string

    while "<" in output and ">" in output and output != previous:
        previous = output
        r = re.compile('<([^<>]*)>')
        full = ""
        m = ""
        # Findall returns a list of str unless it has more than 1 group then it returns as list of match objects. Match is not counted as a group??
        matches = r.findall(output)

        for match in matches:
            # How to return findall with re objects?
            full = "<" + match + ">"

            m = match

            r = re.compile('^[^\\[\\{\\(]*')
            name = r.search(m).group(0)
            

            v = bot_data.get("Variables").get(name)
            if not v: v = bot_data.get("GlobalVariables").get(name)
            if not v: pass

            args = m.replace(name,"")
            
        if v.get("Type") == "Single":
            output = output.replace(full, v.get("Value"))

        elif v.get("Type") == "List":
            if args:
                output = output.replace(full, str(v.get("Value")))

            index = 0
            index = int(ParseArguments(args, "[", "]")[0])
            item = v.get("Value")[index]
            if item:
                output = output.replace(full,item)

        elif v.get("Type") == "Dictionary":
            if "(" in args and ")" in args:
                dicKey = ParseArguments(args, "(", ")")[0]
                # Don't want to change input if this is None
                if v.get("Value").get(dicKey):
                    output = output.replace(full,v.get("Value").get(dicKey))

            elif "{" in args and "}" in args:
                dicVal = ParseArguments(args, "{", "}")[0]
                try:
                    output = [dict_name for dict_name, dict_val in v.get("Value").items() if dicVal == dicVal][0]
                except:
                    pass

            else:
                output = output.replace(full,str(v.get("Value")))
        
    return output


def ReplaceValuesRecursive(input_string,bot_data):
    """
    bot_data = {"Variables": {"SOURCE":{"Value":{"hellow":"meow"},
                                        "Type": "Dictionary",
                                        "Name": "SOURCE"}
                                        },
                "GlobalVariables": {}
                }
    """
    toReplace = []
    r = re.compile('<([^\\[]*)\\[\\*\\]>')
    matches = r.findall(input_string)

    variables = []


    for m in matches:
        name = m

        variable = bot_data.get("Variables").get(name)

        if not variable:
            variable = bot_data.get("GlobalVariables").get(name)
            if not variable:
                break

        if variable.get("Type") == "List":
            variables.append(variable)
            
    def theEnd(toReplace,bot_data):
        return [ReplaceValues(replace,bot_data) for replace in toReplace]


    if len(variables) > 0:
        max_index = len(variable.get("Value"))
        i = 0

        while i < max_index:
            replaced = input_string

            for variable in variables:
                variable_Name = variable.get("Name")
                theList = variable.get("Value")
                if len(theList) > i:
                    replaced = replaced.replace(f"<{variable_Name}[*]>", str(theList[i]))
                else:
                    replaced = replaced.replace(f"<{variable_Name}[*]>", "NULL")

            toReplace.append(replaced)
            i += 1
        return theEnd(toReplace,bot_data)


    r = re.compile("<([^\\(]*)\\(\\*\\)>")
    match = r.match(input_string)

    if match:
        full = match.group(0)
        name = match.group(1)

        theDict = bot_data.get("Variables").get(name)
        if not theDict: theDict = bot_data.get("GlobalVariables").get(name)
        if not theDict: toReplace.append(input_string)
        else:
            for key in theDict.get("Value"):
                aDict = {key,theDict.get("Value")[key]}
                toReplace.append(input_string.replace(full,str(aDict)))
        return theEnd(toReplace, bot_data)
    
    r = re.compile("<([^\\{]*)\\{\\*\\}>")
    match = r.match(input_string)

    if match:
        full = match.group(0)
        name = match.group(1)

        theDict = bot_data.get("Variables").get(name)
        if not theDict: theDict = bot_data.get("GlobalVariables").get(name)
        if not theDict: toReplace.append(input_string)
        else:
            for key in dict(theDict).get("Value"):
                toReplace.append(input_string.replace(full,str(key)))
        return theEnd(toReplace, bot_data)
