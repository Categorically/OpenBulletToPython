from LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier,CheckIdentifier
class BlockKeycheck:
    def __init__(self):
        self.Dict = {}

    def FromLS(self,input_line):
        input_line = input_line.strip()
        line.current = input_line
        if str(input_line).startswith("!"):
            return None
        KeyChains = []
        self.Dict = {}
        
        self.Dict["Booleans"] = {}
        while Lookahead(line.current) == "Boolean":
            boolean_name, boolean_value = SetBool(line.current)
            self.Dict["Booleans"][boolean_name] = boolean_value

        while line.current:
            EnsureIdentifier(line.current,"KEYCHAIN")
            kc = {}
            kc["Keys"] = []
            kc["Type"] = ParseEnum(line.current)
            if kc.get("Type") == "CUSTOM" and Lookahead(line.current) == "Literal":
                kc["CustomType"] = ParseLiteral(line.current)
            kc["Mode"] = ParseEnum(line.current)

            while line.current and line.current.startswith("KEYCHAIN") == False:
                k = {}
                EnsureIdentifier(line.current,"KEY")
                first = ParseLiteral(line.current)

                if CheckIdentifier(line.current,"KEY") or CheckIdentifier(line.current,"KEYCHAIN") or not line.current:
                    k["LeftTerm"] = "<SOURCE>"
                    k["Comparer"] = "Contains"
                    k["RightTerm"] = first
                else:
                    k["LeftTerm"] = first
                    k["Comparer"] = ParseEnum(line.current)
                    if k.get("Comparer") != "Exists" and  k.get("Comparer") != "DoesNotExist":
                        k["RightTerm"] = ParseLiteral(line.current)

                kc["Keys"].append(k)

            KeyChains.append(kc)

        self.Dict["KeyChains"] = KeyChains