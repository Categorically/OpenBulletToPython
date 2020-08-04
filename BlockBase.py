import re
def ParseArguments(input_string, delimL, delimR):
    output = []
    pattern = "\\" + delimL + "([^\\" + delimR + "]*)\\" + delimR
    matches = re.findall(pattern, input_string)
    for match in matches:
        output.append(match)
    return output
bot_data = {"Variables": {"SOURCE":{"Value":{"name":"testes"},
                                                     "Type": "Dictionary"}},
                             "GlobalVariables": {}}
def ReplaceValues(input_string, bot_data):
    """ Example: bot_data = {"Variables": {"SOURCE":{"Value":{"name":"testes"},
                                                     "Type": "Dictionary"}},
                             "GlobalVariables": {}}"""

    if "<" not in input_string and ">" not in input_string: return input_string

    previous = ""
    output = input_string
    
    while "<" in output and ">" in output and output != previous:
        previous = output
        r = re.compile('<([^<>]*)>')
        full = ""
        m = ""
        matches = r.findall(output)

        for match in matches:
            # How to return findall with re objects?
            full = "<" + match + ">"

            m = match

            r = re.compile('^[^\[\{\(]*')
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
                output = output.replace(full,str(item))

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
print(ReplaceValues("<SOURCE>",bot_data))