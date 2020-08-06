from LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier


def ParseString(input_string, separator, count) -> list:
    return [ n.strip() for n in input_string.split(separator,count)]
class BlockRequest:
    def __init__(self):
        self.Dict = {}

    def FromLS(self,input_line):
        input_line = input_line.strip()
        line.current = input_line
        MultipartContents = []
        CustomHeaders = {}
        CustomCookies = {}
        ResponseType = "STRING"

        if str(input_line).startswith("!"):
            return None

        self.Dict = {}

        Method = ParseEnum(line.current)
        self.Dict["Method"] = Method

        Url = ParseLiteral(line.current)
        self.Dict["Url"] = Url

        self.Dict["Booleans"] = {}
        while Lookahead(line.current) == "Boolean":
            boolean_name, boolean_value = SetBool(line.current)
            self.Dict["Booleans"][boolean_name] = boolean_value

        while len(str(line.current)) != 0 and line.current.startswith("->") == False:
            parsed = ParseToken(line.current,"Parameter",True,True).upper()
            if parsed == "MULTIPART":
                self.Dict["RequestType"] = "Multipart"

            elif parsed == "BASICAUTH":
                self.Dict["RequestType"] = "BasicAuth"

            elif parsed == "STANDARD":
                self.Dict["RequestType"] = "Standard"

            elif parsed == "RAW":
                self.Dict["RequestType"] = "Raw"

            elif parsed == "CONTENT":
                PostData = ParseLiteral(line.current)
                self.Dict["PostData"] = PostData

            elif parsed == "RAWDATA":
                RawData = ParseLiteral(line.current)
                self.Dict["RawData"] = RawData

            elif parsed == "STRINGCONTENT":
                stringContentPair = ParseString(ParseLiteral(line.current), ':', 2)
                MultipartContents.append({"Type": "STRING","Name":stringContentPair[0],"Value": stringContentPair[1] })
                
            elif parsed == "FILECONTENT":
                stringContentPair = ParseString(ParseLiteral(line.current), ':', 3)
                MultipartContents.append({"Type": "FILE","Name":stringContentPair[0],"Value": stringContentPair[1] })

            elif parsed == "COOKIE":
                cookiePair = ParseString(ParseLiteral(line.current), ':', 2)
                CustomCookies[cookiePair[0]] = cookiePair[1]

            elif parsed == "HEADER":
                cookiePair = ParseString(ParseLiteral(line.current), ':', 2)
                CustomHeaders[cookiePair[0]] = cookiePair[1]

            elif parsed == "CONTENTTYPE":
                ContentType = ParseLiteral(line.current)
                self.Dict["ContentType"] = ContentType

            elif parsed == "USERNAME":
                AuthUser = ParseLiteral(line.current)
                self.Dict["AuthUser"] = AuthUser

            elif parsed == "PASSWORD":
                AuthPass = ParseLiteral(line.current)
                self.Dict["AuthUser"] = AuthPass


            elif parsed == "BOUNDARY":
                MultipartBoundary = ParseLiteral(line.current)
                self.Dict["MultipartBoundary"] = MultipartBoundary

            elif parsed == "SECPROTO":
                SecurityProtocol = ParseLiteral(line.current)
                self.Dict["SecurityProtocol"] = SecurityProtocol

            else:
                pass

        if line.current.startswith("->"):
            EnsureIdentifier(line.current, "->")
            outType = ParseToken(line.current,"Parameter",True,True)

            if outType.upper() == "STRING":
                ResponseType = "String"

            elif outType.upper() == "File":
                ResponseType = "FILE"
                DownloadPath  = ParseLiteral(line.current)
                self.Dict["DownloadPath"] = DownloadPath
                while Lookahead(line.current) == "Boolean":
                        
                    boolean_name, boolean_value = SetBool(line.current)
                    self.Dict["Booleans"][boolean_name] = boolean_value

            elif outType.upper() == "BASE64":
                ResponseType = "BASE64"
                OutputVariable = ParseLiteral(line.current)
                self.Dict["OutputVariable"] = OutputVariable
                
        self.Dict["CustomCookies"] = CustomCookies
        self.Dict["CustomHeaders"] = CustomHeaders