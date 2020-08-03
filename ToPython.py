from Loliscript import CompressedLines

from BlockParser import Parse

def ToPython(config_text):
    blocks = []
    compressed = CompressedLines(config_text)
    for c in compressed:
        c = Parse(c)
        if c: blocks.append(c)
    return blocks