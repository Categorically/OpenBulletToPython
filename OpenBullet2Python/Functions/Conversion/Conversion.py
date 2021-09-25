import base64

from enum import Enum


class EncodingType(str, Enum):
    HEX = "HEX"
    BIN = "BIN"
    BASE64 = "BASE64"
    ASCII = "ASCII"
    UTF8 = "UTF8"
    UNICODE = "UNICODE"

class Conversion():
    def __init__(self) -> None:
        pass

    def ConvertFrom(self, input_string:str, encoding_type:EncodingType) -> bytes:
        if encoding_type == EncodingType.BASE64:
            inputBytes = input_string.encode('utf-8')
            base64_bytes = base64.b64decode(inputBytes)
            return base64_bytes

        elif encoding_type == EncodingType.HEX:
            return bytes.fromhex(input_string)

        elif encoding_type == EncodingType.BIN:
            numOfBytes = int(len(input_string) / 8)
            output = bytearray(numOfBytes)
            i = 0
            while i < numOfBytes:
                output[i] = int(input_string[8 * i: (8 * i) + 8], 2)
                i += 1
            return bytes(output)

        elif encoding_type == EncodingType.ASCII:
            return input_string.encode(encoding='ascii',errors='replace')

        elif encoding_type == EncodingType.UTF8:
            return input_string.encode(encoding='UTF-8',errors='replace')

        elif encoding_type == EncodingType.UNICODE:
            return input_string.encode(encoding='UTF-16',errors='replace')

    def ConvertTo(self, input_bytes:bytes, encoding_type:EncodingType) -> str:
        if encoding_type == EncodingType.BASE64:
            base64_bytes = base64.b64encode(input_bytes)
            return base64_bytes.decode()

        elif encoding_type == EncodingType.HEX:
            return input_bytes.hex()

        elif encoding_type == EncodingType.BIN:
            output = [f'{byte:0>8b}' for byte in input_bytes]
            return "".join(output)

        elif encoding_type == EncodingType.ASCII:
            return input_bytes.decode(encoding='ascii',errors='replace')

        elif encoding_type == EncodingType.UTF8:
            return input_bytes.decode(encoding='UTF-8',errors='replace')

        elif encoding_type == EncodingType.UNICODE:
            return input_bytes.decode(encoding='UTF-16',errors='replace')

