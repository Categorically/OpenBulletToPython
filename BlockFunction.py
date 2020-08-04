from LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier
class BlockFunction:
    def FromLS(self,input_line):
        input_line = input_line.strip()

        if str(input_line).startswith("!"):
            return None
        line.current = input_line
        function_block = {} 

        function_block["IsCapture"] = False
        
        function_block["VariableName"] = ""

        function_block["InputString"] = ""

        function_block["Booleans"] = {}

        FunctionType  = ParseEnum(line.current)
        function_block["FunctionType"] = FunctionType

        if FunctionType == "Constant":
            pass

        elif FunctionType == "Hash":
            HashType = ParseEnum(line.current)
            function_block["HashType"] = HashType

            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                function_block["Booleans"][boolean_name] = boolean_value
        
        elif FunctionType == "HMAC":
            function_block["HashType"] = ParseEnum(line.current)
            function_block["HmacKey"] = ParseLiteral(line.current)
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                function_block["Booleans"][boolean_name] = boolean_value

        elif FunctionType == "Translate":
            while Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                function_block["Booleans"][boolean_name] = boolean_value
            function_block["TranslationDictionary"] = {}
            while line.current and Lookahead(line.current) == "Parameter":
                EnsureIdentifier(line.current, "KEY")
                k = ParseLiteral(line.current)
                EnsureIdentifier(line.current, "VALUE")
                v = ParseLiteral(line.current)
                function_block["TranslationDictionary"][k] = v

        elif FunctionType == "DateToUnixTime":
            function_block["DateFormat"] = ParseLiteral(line.current)

        elif FunctionType == "UnixTimeToDate":
            function_block["DateFormat"] = ParseLiteral(line.current)
            if Lookahead(line.current) != "Literal":
                function_block["InputString"] = "yyyy-MM-dd:HH-mm-ss"

        elif FunctionType == "Replace":
            function_block["ReplaceWhat"] = ParseLiteral(line.current)
            function_block["ReplaceWith"] = ParseLiteral(line.current)
            if Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                function_block["Booleans"][boolean_name] = boolean_value

        elif FunctionType == "RegexMatch":
            function_block["RegexMatch"] = ParseLiteral(line.current)

        elif FunctionType == "RandomNum":
            if Lookahead(line.current) == "Literal":
                function_block["RandomMin"] = ParseLiteral(line.current)
                function_block["RandomMax"] = ParseLiteral(line.current)
            # Support for old integer definition of Min and Max
            else:
                function_block["RandomMin"] = str(ParseInt(line.current))
                function_block["RandomMax"] = str(ParseInt(line.current))
            
            if Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                function_block["Booleans"][boolean_name] = boolean_value
        
        elif FunctionType == "CountOccurrences":
            function_block["StringToFind"] = ParseLiteral(line.current)

        elif FunctionType == "CharAt":
            function_block["CharIndex"] = ParseLiteral(line.current)

        elif FunctionType == "Substring":
            function_block["SubstringIndex"] = ParseLiteral(line.current)
            function_block["SubstringLength"] = ParseLiteral(line.current)

        elif FunctionType == "RSAEncrypt":
            function_block["RsaN"] = ParseLiteral(line.current)
            function_block["RsaE"] = ParseLiteral(line.current)
            if Lookahead(line.current) == "Boolean":
                boolean_name, boolean_value = SetBool(line.current)
                function_block["Booleans"][boolean_name] = boolean_value

        elif FunctionType == "RSAPKCS1PAD2":
            function_block["RsaN"] = ParseLiteral(line.current)
            function_block["RsaE"] = ParseLiteral(line.current)
        
        elif FunctionType == "GetRandomUA":
            if ParseToken(line.current,"Parameter", False, False) == "BROWSER":
                EnsureIdentifier(line.current,"BROWSER")
                function_block["Booleans"]["UserAgentSpecifyBrowser"] = True
                function_block["UserAgentBrowser"] = ParseEnum(line.current)

        elif FunctionType == "AESDecrypt":
            pass

        elif FunctionType == "AESEncrypt":
            function_block["AesKey"] = ParseLiteral(line.current)
            function_block["AesIV"] = ParseLiteral(line.current)
            function_block["AesMode"] = ParseEnum(line.current)
            function_block["AesPadding"] = ParseEnum(line.current)

        elif FunctionType == "PBKDF2PKCS5":
            if Lookahead(line.current) == "Literal":
                function_block["KdfSalt"] = ParseLiteral(line.current)
            else:
                function_block["KdfSaltSize"] = ParseInt(line.current)
                function_block["KdfIterations"] = ParseInt(line.current)
                function_block["KdfKeySize"] = ParseInt(line.current)
                function_block["KdfAlgorithm"] = ParseEnum(line.current)
                
        else:
            pass
        if Lookahead(line.current) == "Literal":
            function_block["InputString"] = ParseLiteral(line.current)

        # Try to parse the arrow, otherwise just return the block as is with default var name and var / cap choice
        if not ParseToken(line.current,"Arrow",False,True):
            return function_block
            
        # Parse the VAR / CAP
        varType = ParseToken(line.current,"Parameter",True,True)
        if str(varType.upper()) == "VAR" or str(varType.upper()) == "CAP":
            if str(varType.upper()) == "CAP": function_block["IsCapture"] = True

        # Parse the variable/capture name
        function_block["VariableName"] = ParseToken(line.current,"Literal",True,True)

        return function_block
