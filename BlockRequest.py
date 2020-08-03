from LineParser import ParseLabel,ParseEnum,ParseLiteral, line,Lookahead, SetBool,ParseToken,ParseInt,EnsureIdentifier


def ParseString(input_string, separator, count) -> dict:
    return [ n.strip() for n in input_string.split(separator,count)]

def FromLS(input_line):
    line_input = input_line.strip()
    line.current = input_line
    MultipartContents = []
    CustomHeaders = {}
    CustomCookies = {}
    ResponseType = "STRING"

    if str(line_input).startswith("!"):
        return None
    
    request_block = {}

    #Temp
    if input_line.startswith("#"):
        label = ParseLabel(line.current)
        request_block["label"] = label

    #Temp
    block_type = ParseEnum(line.current)
    request_block["block_type"] = block_type

    Method = ParseEnum(line.current)
    request_block["Method"] = Method

    Url = ParseLiteral(line.current)
    request_block["Url"] = Url

    Booleans = {}
    while Lookahead(line.current) == "Boolean":
        boolean_name, boolean_value = SetBool(line.current)
        Booleans[boolean_name] = boolean_value
    request_block["Booleans"] = Booleans

    while len(str(line.current)) != 0 and line.current.startswith("->") == False:
        parsed = ParseToken(line.current,"Parameter",True,True).upper()
        if parsed == "MULTIPART":
            request_block["Multipart"] = True

        elif parsed == "BASICAUTH":
            request_block["Multipart"] = True

        elif parsed == "STANDARD":
            request_block["Multipart"] = True

        elif parsed == "RAW":
            request_block["Multipart"] = True

        elif parsed == "CONTENT":
            PostData = ParseLiteral(line.current)
            request_block["PostData"] = PostData

        elif parsed == "RAWDATA":
            RawData = ParseLiteral(line.current)
            request_block["RawData"] = RawData

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
            request_block["ContentType"] = ContentType

        elif parsed == "USERNAME":
            AuthUser = ParseLiteral(line.current)
            request_block["AuthUser"] = AuthUser

        elif parsed == "PASSWORD":
            AuthPass = ParseLiteral(line.current)
            request_block["AuthUser"] = AuthPass


        elif parsed == "BOUNDARY":
            MultipartBoundary = ParseLiteral(line.current)
            request_block["MultipartBoundary"] = MultipartBoundary

        elif parsed == "SECPROTO":
            SecurityProtocol = ParseLiteral(line.current)
            request_block["SecurityProtocol"] = SecurityProtocol

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
            request_block["DownloadPath"] = DownloadPath
            while Lookahead(line.current) == "Boolean":
                    
                boolean_name, boolean_value = SetBool(line.current)
                Booleans[boolean_name] = boolean_value
            request_block["Booleans"] = Booleans

        elif outType.upper() == "BASE64":
            ResponseType = "BASE64"
            OutputVariable = ParseLiteral(line.current)
            request_block["OutputVariable"] = OutputVariable
            
    request_block["CustomCookies"] = CustomCookies
    request_block["CustomHeaders"] = CustomHeaders
    return request_block