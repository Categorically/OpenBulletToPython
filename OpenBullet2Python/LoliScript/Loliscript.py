
from OpenBullet2Python.LoliScript.BlockParser import IsBlock

def CompressedLines(config_text) -> list:
    i = 0
    isScript = False
    compressed = config_text.splitlines()
    while i < len(compressed) - 1 :
        if isScript == False and IsBlock(compressed[i]) and compressed[i + 1].startswith(" ") or compressed[i + 1].startswith("\t"):
            compressed[i] += " " + compressed[i + 1].strip()
            compressed.pop(i + 1)
        elif isScript == False and IsBlock(compressed[i]) and compressed[i + 1].startswith("! ") or compressed[i + 1].startswith("!\t"):
            compressed[i] += " " + compressed[i + 1][1:].strip()
            compressed.pop(i + 1)
        else:
            if compressed[i].startswith("BEGIN SCRIPT"):
                isScript = True
            elif compressed[i].startswith("END SCRIPT"):
                isScript = False

            i += 1
    return compressed