from LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken

def FromLS(input_line):
    line_input = input_line.strip()
    line.current = input_line
    if str(line_input).startswith("!"):
        return None
    
    parse_block = {}
    label = ParseLabel(line.current)
    print(f"label: {label}")
    parse_block["label"] = label

    block_type = ParseEnum(line.current)
    print(f"block_type: {block_type}")
    parse_block["block_type"] = block_type

    ParseTarget = ParseLiteral(line.current)
    parse_block["ParseTarget"] = ParseTarget
    print(f"ParseTarget: {ParseTarget}")

    parse_type = ParseEnum(line.current)
    parse_block["parse_type"] = parse_type
    print(f"parse_type: {parse_type}")
    if parse_type == "REGEX":

        regex_pattern  = ParseLiteral(line.current)
        print(f"regex_pattern: {regex_pattern}")
        parse_block["regex_pattern"] = regex_pattern

        regex_output = ParseLiteral(line.current)
        print(f"regex_output: {regex_output}")
        parse_block["regex_output"] = regex_output

        Booleans = {}
        while Lookahead(line.current) == "Boolean":
            boolean_name, boolean_value = SetBool(line.current)
            Booleans[boolean_name] = boolean_value
        print(f"Booleans: {Booleans}")
        parse_block["Booleans"] = Booleans
    else:
        return None
    arrow = ParseToken(line.current,"Arrow",True,True)
    print(f"arrow: {arrow}")

    var_type = ParseToken(line.current,"Parameter",True,True)
    print(f"var_type: {var_type}")
    IsCapture = False
    if str(var_type.upper()) == "VAR" or str(var_type.upper()) == "CAP":
        if str(var_type.upper()) == "CAP": IsCapture = True
    print(f"IsCapture: {IsCapture}")
    parse_block["IsCapture"] = IsCapture

    variable_name = ParseLiteral(line.current)
    print(f"variable_name: {variable_name}")
    parse_block["variable_name"] = variable_name

    prefix = ParseLiteral(line.current)
    print(f"prefix: {prefix}")
    parse_block["prefix"] = prefix

    suffix = ParseLiteral(line.current)
    print(f"suffix: {suffix}")
    parse_block["suffix"] = suffix
    print(parse_block)
    return parse_block