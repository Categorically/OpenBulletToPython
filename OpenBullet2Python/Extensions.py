import os

def IsSubPathOf(parent_path, child_path):
    parent_path = os.path.abspath(os.path.realpath(parent_path))
    child_path = os.path.abspath(os.path.realpath(child_path))

    return os.path.commonpath([parent_path]) == os.path.commonpath([parent_path, child_path])
