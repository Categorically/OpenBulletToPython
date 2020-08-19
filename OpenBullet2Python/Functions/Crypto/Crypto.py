import hashlib
import hmac
#This might clash with Crypto lib
class Crypto:
    def MD5(self,rawInput):
        h = hashlib.md5()
        h.update(rawInput)
        return h.digest()

    def SHA1(self,rawInput):
        h = hashlib.sha1()
        h.update(rawInput)
        return h.digest()

    def SHA256(self,rawInput):
        h = hashlib.sha256()
        h.update(rawInput)
        return h.digest()

    def SHA384(self,rawInput):
        h = hashlib.sha384()
        h.update(rawInput)
        return h.digest()

    def SHA512(self,rawInput):
        h = hashlib.sha512()
        h.update(rawInput)
        return h.digest()



    def HMACMD5(self,rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.md5).digest()

    def HMACSHA1(self,rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha1).digest()

    def HMACSHA256(self,rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha256).digest()

    def HMACSHA384(self,rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha384).digest()
        
    def HMACSHA512(self,rawInput,rawKey):
        return hmac.new(rawKey, rawInput, hashlib.sha512).digest()