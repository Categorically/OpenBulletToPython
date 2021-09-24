from OpenBullet2Python.Extensions import IsSubPathOf
def NotInCWD(cwd, path):
    return not IsSubPathOf(cwd, path)