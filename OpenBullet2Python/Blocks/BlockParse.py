from OpenBullet2Python.LoliScript.LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt

from OpenBullet2Python.Blocks.BlockBase import ReplaceValues,InsertVariable

from OpenBullet2Python.Functions.Parsing.Parse import LR, JSON
class ParseType:
    LR = "LR"
    CSS = "CSS"
    JSON = "JSON"
    REGEX = "REGEX"
class BlockParse:
    def __init__(self):
        self.VariableName  = ""  
        self.IsCapture  = False 
        self.ParseTarget = "" 
        self.Prefix = ""
        self.Suffix = ""
        self.Recursive = False
        self.DotMatches = False
        self.CaseSensitive  = True
        self.EncodeOutput = False
        self.CreateEmpty = True
        self.ParseType = ""

        # LR
        self.LeftString = ""
        self.RightString = ""
        self.UseRegexLR = False

        # CSS
        self.CssSelector = ""
        self.AttributeName = ""
        self.CssElementIndex = 0

        # JSON
        self.JsonField = ""
        self.JTokenParsing = False

        # REGEX
        self.RegexString = ""
        self.RegexOutput = ""



        self.Dict = None

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
        self.ParseTarget = ParseTarget

        parse_type = ParseEnum(line.current)
        self.Dict["parse_type"] = parse_type
        self.ParseType = parse_type

        if parse_type == ParseType().REGEX:
            regex_pattern  = ParseLiteral(line.current)
            self.Dict["regex_pattern"] = regex_pattern

            regex_output = ParseLiteral(line.current)
            self.Dict["regex_output"] = regex_output

            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif parse_type == ParseType().CSS:
            CssSelector =  ParseLiteral(line.current)
            self.Dict["CssSelector"] = CssSelector

            AttributeName = ParseLiteral(line.current)
            self.Dict["AttributeName"] = AttributeName

            if Lookahead(line.current) == "Boolean":
                SetBool(line.current,self)
            elif Lookahead(line.current) == "Integer":
                CssElementIndex = ParseInt(line.current)
                self.Dict["CssElementIndex"] = CssElementIndex
            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif parse_type == ParseType().JSON:
            JsonField = ParseLiteral(line.current)
            self.Dict["JsonField"] = JsonField
            self.JsonField = JsonField
            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
                
        elif parse_type == ParseType().LR:
            LeftString = ParseLiteral(line.current)
            self.Dict["LeftString"] = LeftString
            self.LeftString = LeftString
            RightString = ParseLiteral(line.current)
            self.RightString = RightString
            self.Dict["RightString"] = RightString
            self.Dict["Booleans"] = {}
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        else:
            return None

        arrow = ParseToken(line.current,"Arrow",True,True)

        var_type = ParseToken(line.current,"Parameter",True,True)

        IsCapture = False
        if str(var_type.upper()) == "VAR" or str(var_type.upper()) == "CAP":
            if str(var_type.upper()) == "CAP": IsCapture = True
        self.Dict["IsCapture"] = IsCapture
        self.IsCapture = IsCapture
        
        variable_name = ParseLiteral(line.current)
        self.Dict["variable_name"] = variable_name
        self.VariableName = variable_name

        prefix = ParseLiteral(line.current)
        self.Dict["prefix"] = prefix
        self.Prefix = prefix

        suffix = ParseLiteral(line.current)
        self.Dict["suffix"] = suffix
        self.Suffix = suffix

    def Process(self,BotData):
        original = ReplaceValues(self.ParseTarget,BotData)
        List = []
        if self.ParseType == ParseType().LR:
            List = LR(original,ReplaceValues(self.LeftString,BotData),ReplaceValues(self.RightString,BotData),self.Recursive,self.UseRegexLR)
            print(f"Parsed LR {List} From {original[0:10]}......")
        elif self.ParseType == ParseType().JSON:
            List = JSON(original,ReplaceValues(self.JsonField,BotData),self.Recursive,self.JTokenParsing)
            print(f"Parsed JSON {List} From {original[0:10]}......")
        else:
            pass

        InsertVariable(BotData,self.IsCapture,self.Recursive,List,self.VariableName,self.Prefix,self.Suffix,self.EncodeOutput,self.CreateEmpty)
