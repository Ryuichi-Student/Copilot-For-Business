import re

def clean_name(name):
    name = re.sub(r"[^\w\s]", '', name)
    name = re.sub(r"\s+", '_', name)
    return "_" + name

def natural_name(name):
    name = re.sub('_', " ", name)
    name = name.title()
    return name