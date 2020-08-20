from OpenBullet2Python.LoliScript.Loliscript import CompressedLines

from OpenBullet2Python.LoliScript.BlockParser import Parse

def ToPython(config_text):
    blocks = []
    compressed = CompressedLines(config_text)
    for c in compressed:
        c = Parse(c)
        if c: blocks.append(c.Dict)
    return blocks