import hashlib
from hashlib import pbkdf2_hmac
import hmac
from enum import Enum
import base64
from secrets import token_bytes

class Hash(str, Enum):
    MD4 = "MD4"
    MD5 = "MD5"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    SHA512 = "SHA512"

class Crypto:

    def PBKDF2PKCS5(password:str, salt:str = None, saltSize:int = 8, iterations:int = 1, keyLength:str = 16, type:Hash = Hash.SHA1):
        if salt:
            deriveBytes = pbkdf2_hmac(
                hash_name = type.lower(), 
                password = str.encode(password),
                salt = base64.b64decode(salt), 
                iterations = iterations, 
                dklen = keyLength
            )
            return base64.b64encode(deriveBytes).decode()
        else:
            deriveBytes = pbkdf2_hmac(
                hash_name = type.lower(), 
                password = str.encode(password),
                salt = token_bytes(saltSize), 
                iterations = iterations,
                dklen = keyLength
            )
            return base64.b64encode(deriveBytes).decode()
            
    def MD4(rawInput):
        h = hashlib.new('md4')
        h.update(rawInput)
        return h.digest()
    def MD5(rawInput):
        h = hashlib.md5()
        h.update(rawInput)
        return h.digest()

    def SHA1(rawInput):
        h = hashlib.sha1()
        h.update(rawInput)
        return h.digest()

    def SHA256(rawInput):
        h = hashlib.sha256()
        h.update(rawInput)
        return h.digest()

    def SHA384(rawInput):
        h = hashlib.sha384()
        h.update(rawInput)
        return h.digest()

    def SHA512(rawInput):
        h = hashlib.sha512()
        h.update(rawInput)
        return h.digest()


    def HMACMD5(rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.md5).digest()

    def HMACSHA1(rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha1).digest()

    def HMACSHA256(rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha256).digest()

    def HMACSHA384(rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha384).digest()
        
    def HMACSHA512(rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha512).digest()