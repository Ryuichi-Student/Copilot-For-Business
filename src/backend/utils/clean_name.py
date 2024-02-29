import re

def clean_name(name):
    name = re.sub(r"[^\w\s]", '', name)
    name = re.sub(r"\s+", '_', name)
    return "_" + name