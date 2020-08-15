import hashlib
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

