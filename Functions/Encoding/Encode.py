import base64

def ToBase64(inputString:str):
    inputBytes = inputString.encode('utf-8')
    base64_bytes = base64.b64encode(inputBytes)
    return base64_bytes.decode('utf-8')


def FromBase64(base64EncodedData):
    base64EncodedBytes = base64EncodedData.encode('utf-8')
    base64_bytes = base64.b64decode(base64EncodedBytes)
    return base64_bytes.decode('utf-8')
