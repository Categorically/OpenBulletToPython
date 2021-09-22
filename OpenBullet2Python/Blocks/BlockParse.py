from OpenBullet2Python.LoliScript.LineParser import LineParser, ParseLabel,ParseEnum,ParseLiteral,Lookahead, SetBool,ParseToken,ParseInt

from OpenBullet2Python.Blocks.BlockBase import ReplaceValues,InsertVariable

from OpenBullet2Python.Functions.Parsing.Parse import LR, JSON, REGEX
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

    def FromLS(self, line:LineParser):

        if str(line.current).startswith("!"):
            return None

        self.Dict = {}

        ParseTarget = ParseLiteral(line)
        self.Dict["ParseTarget"] = ParseTarget
        self.ParseTarget = ParseTarget

        parse_type = ParseEnum(line)
        self.Dict["parse_type"] = parse_type
        self.ParseType = parse_type

        if parse_type == ParseType().REGEX:
            regex_pattern  = ParseLiteral(line)
            self.Dict["regex_pattern"] = regex_pattern
            self.RegexString = regex_pattern

            regex_output = ParseLiteral(line)
            self.Dict["regex_output"] = regex_output
            self.RegexOutput = regex_output

            self.Dict["Booleans"] = {}
            while Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
        
        elif parse_type == ParseType().CSS:
            CssSelector =  ParseLiteral(line)
            self.Dict["CssSelector"] = CssSelector

            AttributeName = ParseLiteral(line)
            self.Dict["AttributeName"] = AttributeName

            if Lookahead(line) == "Boolean":
                SetBool(line,self)
            elif Lookahead(line) == "Integer":
                CssElementIndex = ParseInt(line)
                self.Dict["CssElementIndex"] = CssElementIndex
            self.Dict["Booleans"] = {}
            while Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        elif parse_type == ParseType().JSON:
            JsonField = ParseLiteral(line)
            self.Dict["JsonField"] = JsonField
            self.JsonField = JsonField
            self.Dict["Booleans"] = {}
            while Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value
                
        elif parse_type == ParseType().LR:
            LeftString = ParseLiteral(line)
            self.Dict["LeftString"] = LeftString
            self.LeftString = LeftString
            RightString = ParseLiteral(line)
            self.RightString = RightString
            self.Dict["RightString"] = RightString
            self.Dict["Booleans"] = {}
            while Lookahead(line) == "Boolean":
                boolean_name, boolean_value = SetBool(line,self)
                self.Dict["Booleans"][boolean_name] = boolean_value

        else:
            return None

        arrow = ParseToken(line,"Arrow",True,True)

        var_type = ParseToken(line,"Parameter",True,True)

        IsCapture = False
        if str(var_type.upper()) == "VAR" or str(var_type.upper()) == "CAP":
            if str(var_type.upper()) == "CAP": IsCapture = True
        self.Dict["IsCapture"] = IsCapture
        self.IsCapture = IsCapture
        
        variable_name = ParseLiteral(line)
        self.Dict["variable_name"] = variable_name
        self.VariableName = variable_name

        prefix = ParseLiteral(line)
        self.Dict["prefix"] = prefix
        self.Prefix = prefix

        suffix = ParseLiteral(line)
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
        elif self.ParseType == ParseType().REGEX:
            List = REGEX(original,ReplaceValues(self.RegexString,BotData),ReplaceValues(self.RegexOutput,BotData),self.Recursive)
            print(f"Parsed REGEX {List} From {original[0:10]}......")
        else:
            pass

        InsertVariable(BotData,self.IsCapture,self.Recursive,List,self.VariableName,self.Prefix,self.Suffix,self.EncodeOutput,self.CreateEmpty)
