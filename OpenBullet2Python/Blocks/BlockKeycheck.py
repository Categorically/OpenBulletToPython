from OpenBullet2Python.LoliScript.LineParser import LineParser, ParseLabel,ParseEnum,ParseLiteral,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier,CheckIdentifier
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
    def FromLS(self,line:LineParser):
        if str(line.current).startswith("!"):
            return None
        KeyChains = []
        self.KeyChains_Objects = []
        self.Dict = {}
        
        self.Dict["Booleans"] = {}
        while Lookahead(line) == "Boolean":
            boolean_name, boolean_value = SetBool(line,self)
            self.Dict["Booleans"][boolean_name] = boolean_value

        while line.current:
            EnsureIdentifier(line,"KEYCHAIN")
            KC = KeyChain()
            kc = {}
            kc["Keys"] = []
            KeyChainType = ParseEnum(line)
            
            kc["Type"] = KeyChainType
            KC.Type = KeychainType[KeyChainType]
            if kc.get("Type") == "CUSTOM" and Lookahead(line) == "Literal":
                kc["CustomType"] = ParseLiteral(line)
            # kc["Mode"] = ParseEnum(line)
            KC_Mode = ParseEnum(line)
            kc["Mode"] = KC_Mode
            KC.Mode = KeychainMode[KC_Mode]

            while line.current and line.current.startswith("KEYCHAIN") == False:
                k = {}
                Key_Object = Key()
                EnsureIdentifier(line,"KEY")
                first = ParseLiteral(line)

                if CheckIdentifier(line,"KEY") or CheckIdentifier(line,"KEYCHAIN") or not line.current:
                    Key_Object.LeftTerm = "<SOURCE>"
                    Key_Object.Comparer = Comparer["Contains"]
                    Key_Object.RightTerm = first
                    k["LeftTerm"] = "<SOURCE>"
                    k["Comparer"] = "Contains"
                    k["RightTerm"] = first
                else:
                    Key_Object.LeftTerm = first
                    k["LeftTerm"] = first
                    Comparer__ = ParseEnum(line)
                    k["Comparer"] = Comparer__
                    Key_Object.Comparer = Comparer[Comparer__]
                    if Key_Object.Comparer.value != "Exists" and  Key_Object.Comparer.value != "DoesNotExist":
                        RightTerm__ = ParseLiteral(line)
                        k["RightTerm"] = RightTerm__
                        Key_Object.RightTerm = RightTerm__
                KC.Keys.append(Key_Object)
                kc["Keys"].append(k)
            self.KeyChains_Objects.append(KC)
            KeyChains.append(kc)

        self.Dict["KeyChains"] = KeyChains

    def Process(self,BotData):
        try:
            if BotData.ResponseCodeGet().startswith("4") and self.banOn4XX:
                BotData.status = BotData.BotStatus.BAN
                return
        except Exception:
            pass
        

        found = False

        for keychain in self.KeyChains_Objects:
            if keychain.CheckKeys(BotData):
                found = True
                if keychain.Type == KeychainType.Success:
                    BotData.status = BotData.BotStatus.SUCCESS
                elif keychain.Type == KeychainType.Failure:
                    BotData.status = BotData.BotStatus.FAIL
                elif keychain.Type == KeychainType.Ban:
                    BotData.status = BotData.BotStatus.BAN

        if not found and self.banOnToCheck:
            BotData.status = BotData.BotStatus.BAN