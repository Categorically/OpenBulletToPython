from Extensions import IsSubPathOf
def NotInCWD(cwd, path):
    return not IsSubPathOf(cwd, path)