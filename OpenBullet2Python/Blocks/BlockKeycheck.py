from OpenBullet2Python.LoliScript.LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier,CheckIdentifier
from OpenBullet2Python.Models.KeyChain import KeychainType, KeychainMode, KeyChain
from OpenBullet2Python.Models.Key import Key
from OpenBullet2Python.Functions.Conditions.Condition import Comparer
from OpenBullet2Python.Models.BotData import BotData
class BlockKeycheck:
    def __init__(self):
        self.Dict = {}
        self.KeyChains_Objects = []
        self.banOnToCheck = True
        self.banOn4XX = False
    def FromLS(self,input_line):
        input_line = input_line.strip()
        line.current = input_line
        if str(input_line).startswith("!"):
            return None
        KeyChains = []
        self.KeyChains_Objects = []
        self.Dict = {}
        
        self.Dict["Booleans"] = {}
        while Lookahead(line.current) == "Boolean":
            boolean_name, boolean_value = SetBool(line.current,self)
            self.Dict["Booleans"][boolean_name] = boolean_value

        while line.current:
            EnsureIdentifier(line.current,"KEYCHAIN")
            KC = KeyChain()
            kc = {}
            kc["Keys"] = []
            KeyChainType = ParseEnum(line.current)
            
            kc["Type"] = KeyChainType
            KC.Type = KeychainType[KeyChainType]
            if kc.get("Type") == "CUSTOM" and Lookahead(line.current) == "Literal":
                kc["CustomType"] = ParseLiteral(line.current)
            # kc["Mode"] = ParseEnum(line.current)
            KC_Mode = ParseEnum(line.current)
            kc["Mode"] = KC_Mode
            KC.Mode = KeychainMode[KC_Mode]

            while line.current and line.current.startswith("KEYCHAIN") == False:
                k = {}
                Key_Object = Key()
                EnsureIdentifier(line.current,"KEY")
                first = ParseLiteral(line.current)

                if CheckIdentifier(line.current,"KEY") or CheckIdentifier(line.current,"KEYCHAIN") or not line.current:
                    Key_Object.LeftTerm = "<SOURCE>"
                    Key_Object.Comparer = Comparer["Contains"]
                    Key_Object.RightTerm = first
                    k["LeftTerm"] = "<SOURCE>"
                    k["Comparer"] = "Contains"
                    k["RightTerm"] = first
                else:
                    Key_Object.LeftTerm = first
                    k["LeftTerm"] = first
                    Comparer__ = ParseEnum(line.current)
                    k["Comparer"] = Comparer__
                    Key_Object.Comparer = Comparer[Comparer__]
                    if Key_Object.Comparer.value != "Exists" and  Key_Object.Comparer.value != "DoesNotExist":
                        RightTerm__ = ParseLiteral(line.current)
                        k["RightTerm"] = RightTerm__
                        Key_Object.RightTerm = RightTerm__
                KC.Keys.append(Key_Object)
                kc["Keys"].append(k)
            self.KeyChains_Objects.append(KC)
            KeyChains.append(kc)

        self.Dict["KeyChains"] = KeyChains

    def Process(self):
        try:
            if BotData.ResponseCode().get().startswith("4") and self.banOn4XX:
                BotData.Status = BotData.BotStatus.BAN
                return
        except:
            pass
        

        found = False

        for keychain in self.KeyChains_Objects:
            if keychain.CheckKeys():
                found = True
                if keychain.Type == KeychainType.Success:
                    BotData.Status = BotData.BotStatus.SUCCESS
                elif keychain.Type == KeychainType.Failure:
                    BotData.Status = BotData.BotStatus.FAIL
                elif keychain.Type == KeychainType.Ban:
                    BotData.Status = BotData.BotStatus.BAN

        if not found and self.banOnToCheck:
            BotData.Status = BotData().BotStatus.BAN