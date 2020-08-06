from LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt
class ParseType:
    LR = "LR"
    CSS = "CSS"
    JSON = "JSON"
    REGEX = "REGEX"
class BlockParse:
    def __init__(self,parseTarget="<SOURCE>",prefix="",suffix="",recursive=False,variableName=None, isCapture=False,inputString="",functionType=None,Dict=None,dotMatches=False,caseSensitive=False,createEmpty=True,ParseType=ParseType().LR):
        self.variableName = variableName 
        self.isCapture = isCapture 
        self.parseTarget = parseTarget
        self.prefix = prefix
        self.suffix = suffix
        self.recursive = recursive
        self.dotMatches = dotMatches
        self.caseSensitive = caseSensitive
        self.createEmpty = createEmpty
        self.ParseType = ParseType

        #LR
        self.leftString = ""
        self.rightString = ""
        self.useRegexLR = ""

        #CSS
        self.cssSelector = ""
        self.attributeName = ""
        self.cssElementIndex = 0

        #JSON
        self.jsonField = ""
        self.jTokenParsing = False

        #REGEX
        self.regexString = ""
        self.regexOutput = ""



        self.Dict = Dict

    def FromLS(self,input_line) -> dict:
        """
        "<SOURCE>" REGEX "" "" CreateEmpty=FALSE -> VAR ""
        """
        input_line = input_line.strip()

        if str(input_line).startswith("!"):
            return None
        line.current = input_line
        self.Dict = {}

        ParseTarget = ParseLiteral(line.current)
        self.Dict["ParseTarget"] = ParseTarget

        parse_type = ParseEnum(line.current)
        self.Dict["parse_type"] = parse_type

        if parse_type == "REGEX":
            regex_pattern  = ParseLiteral(line.current)
            self.Dict["regex_pattern"] = regex_pattern

            regex_output = ParseLiteral(line.current)
            self.Dict["regex_output"] = regex_output

            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif parse_type == "CSS":
            CssSelector =  ParseLiteral(line.current)
            self.Dict["CssSelector"] = CssSelector

            AttributeName = ParseLiteral(line.current)
            self.Dict["AttributeName"] = AttributeName

            if Lookahead(line.current) == "Boolean":
                SetBool(line.current)
            elif Lookahead(line.current) == "Integer":
                CssElementIndex = ParseInt(line.current)
                self.Dict["CssElementIndex"] = CssElementIndex
            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif parse_type == "JSON":
            JsonField = ParseLiteral(line.current)
            self.Dict["JsonField"] = JsonField
            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif parse_type == "LR":
            LeftString = ParseLiteral(line.current)
            self.Dict["LeftString"] = LeftString
            RightString = ParseLiteral(line.current)
            self.Dict["RightString"] = RightString
            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                self.Dict["Booleans"][boolean_name] = boolean_value

        else:
            return None

        arrow = ParseToken(line.current,"Arrow",True,True)

        var_type = ParseToken(line.current,"Parameter",True,True)

        IsCapture = False
        if str(var_type.upper()) == "VAR" or str(var_type.upper()) == "CAP":
            if str(var_type.upper()) == "CAP": IsCapture = True
        self.Dict["IsCapture"] = IsCapture

        variable_name = ParseLiteral(line.current)
        self.Dict["variable_name"] = variable_name

        prefix = ParseLiteral(line.current)
        self.Dict["prefix"] = prefix

        suffix = ParseLiteral(line.current)
        self.Dict["suffix"] = suffix