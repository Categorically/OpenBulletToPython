from LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt
class BlockParse:
    def FromLS(self,input_line) -> dict:
        """
        "<SOURCE>" REGEX "" "" CreateEmpty=FALSE -> VAR ""
        """
        input_line = input_line.strip()

        if str(input_line).startswith("!"):
            return None
        line.current = input_line
        parse_block = {}

        ParseTarget = ParseLiteral(line.current)
        parse_block["ParseTarget"] = ParseTarget

        parse_type = ParseEnum(line.current)
        parse_block["parse_type"] = parse_type

        if parse_type == "REGEX":
            regex_pattern  = ParseLiteral(line.current)
            parse_block["regex_pattern"] = regex_pattern

            regex_output = ParseLiteral(line.current)
            parse_block["regex_output"] = regex_output

            parse_block["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                parse_block["Booleans"][boolean_name] = boolean_value
        
        elif parse_type == "CSS":
            CssSelector =  ParseLiteral(line.current)
            parse_block["CssSelector"] = CssSelector

            AttributeName = ParseLiteral(line.current)
            parse_block["AttributeName"] = AttributeName

            if Lookahead(line.current) == "Boolean":
                SetBool(line.current)
            elif Lookahead(line.current) == "Integer":
                CssElementIndex = ParseInt(line.current)
                parse_block["CssElementIndex"] = CssElementIndex
            parse_block["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                parse_block["Booleans"][boolean_name] = boolean_value

        elif parse_type == "JSON":
            JsonField = ParseLiteral(line.current)
            parse_block["JsonField"] = JsonField
            parse_block["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                parse_block["Booleans"][boolean_name] = boolean_value

        elif parse_type == "LR":
            LeftString = ParseLiteral(line.current)
            parse_block["LeftString"] = LeftString
            RightString = ParseLiteral(line.current)
            parse_block["RightString"] = RightString
            parse_block["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                parse_block["Booleans"][boolean_name] = boolean_value

        else:
            return None

        arrow = ParseToken(line.current,"Arrow",True,True)

        var_type = ParseToken(line.current,"Parameter",True,True)

        IsCapture = False
        if str(var_type.upper()) == "VAR" or str(var_type.upper()) == "CAP":
            if str(var_type.upper()) == "CAP": IsCapture = True
        parse_block["IsCapture"] = IsCapture

        variable_name = ParseLiteral(line.current)
        parse_block["variable_name"] = variable_name

        prefix = ParseLiteral(line.current)
        parse_block["prefix"] = prefix

        suffix = ParseLiteral(line.current)
        parse_block["suffix"] = suffix

        return parse_block