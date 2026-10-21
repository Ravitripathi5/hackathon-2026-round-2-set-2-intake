import os

def store_path(base, name):
    # name comes from the object key suffix
    return os.path.join(base, name)
