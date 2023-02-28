import json
import shutil
from pathlib import Path, PurePosixPath
import os

data=None
defmap={}
filePath = Path(os.path.realpath(__file__))
fsroot = filePath.parents[4]
folder = filePath.parent
tmp = folder / "tmp"

fsroot_modules = fsroot / "src/modules"

def posix_path(s): return str(PurePosixPath(s)).replace("\\", "")

def merge_json():
    files= ["raylib", "rlgl", "raymath",  "raygui"]

    merged= {
        'defines':   [],
        'structs':   [],
        'aliases':   [],
        'enums':     [],
        'callbacks': [],
        'functions': []
    }

    for file in files:
        with open(fsroot_modules / f"cpython/cpygen/tmp/{file}.h.json") as f:  
            data = json.load(f)
            for key in ["defines", "structs", "aliases", "enums", "callbacks", "functions"]:
                merged[key].extend(data[key])

    return merged

def load_json():
    global data, aliases, typemap

    #with open(fsroot_modules / "cpython/cpygen/tmp/raylib.h.json") as f:  
    #    data = json.load(f)

    data = merge_json()
    
    # Aliases store 'alternate' names for symbols. We'll store these
    # So that if any are encountered we can swap for the 'real' name
    for i in data["aliases"]: 
        aliases[i["name"]] = i["type"] # This is standalone list for reference
        typemap[i["name"]] = i["type"] # This is modifying list of types for conversions

    # Next we cache most symbols into a lookup map 'defmap' so we can quickly
    # find them later for analysis during various codegen steps.

    for i in data["functions"]:
        defmap[i["name"]] = i
    
    for i in data["structs"]:
        defmap[i["name"]] = i
        for j in i["fields"]:
            defmap[i["name"]+"_"+j["name"]] = j
        
    for i in data["aliases"]: defmap[i["name"]] = defmap[i["type"]]
    

basictypes = ["int", "float", "str", "bool"]

sstypemap = {
    "int":"__ss_int",
    "float":"__ss_float",
    "bool":"__ss_int",# __ss_bool doesnt cast as its a class
}

typemap = {
    "float *": "FloatList",
    "const float *": "FloatList",
    "unsigned char *": "IntList",
    "const unsigned char *": "VoidPtr",
    "char *": "str",
    "const char *": "str",
    "char **": "StrList",
    "unsigned short *": "IntList",
    "unsigned int *": "IntList",
    "int *": "IntList",
    "const int *": "IntList",    
    "void *": "VoidPtr",

    "double": "float",
    "unsigned char": "int",
    "unsigned int": "int",
    "unsigned short": "int",
    "rAudioBuffer *": "VoidPtr",
    "rAudioProcessor *": "VoidPtr",
    "void": "None",
    "va_list": "VoidPtr",
    "long": "int",
    "...": "StrList",
    "char": "str",
}

defaults = {
    "int": "0",
    "float": "0.0",
    "str": '""',
    "bool": "False"
}

def calctype(t):
    global typemap

    if t in typemap.keys():
        return typemap[t]
    
    t = t.replace("const ", "")
    if t.endswith("**"): t=t.replace("**", "*")
    if t.endswith("]"): t=t.split("[")[0] + " *"

    if t in typemap.keys():
        return typemap[t]
    
    if t.endswith("*"):
        return calctype(t.split(" ")[0]) + "List"

    if t in typemap.keys():
        return typemap[t]
    
    return t

ptrs = {
    "float": "SSFloatPtr", 
    "const float": "SSFloatPtr", 
    "double": "SSDoublePtr", 
    "int": "SSIntPtr", 
    "unsigned int": "SSUIntPtr", 
    "const int": "SSIntPtr",   
    "short": "SSShortPtr", 
    "unsigned short": "SSUShortPtr", 
    "char": "SSCharPtr", 
    "unsigned char": "SSUCharPtr", 
}

def ptrType(ctype):
    
    t = calcListType(ctype)
    
    ret = t
    if t in ptrs.keys(): ret = ptrs[t]
    if ret.startswith("const"): ret = ret[6:]
    if ret in aliases.keys(): ret = aliases[ret]
    return ret

def maptype(t):
    
    result = calctype(t)
    
    if result.endswith("List") and result not in defmap.keys(): return ptrType(t)
    if result in aliases.keys(): result = aliases[result]
    return result

def isList(ctype):
    result = calctype(ctype)
    return result.endswith("List") and result not in defmap.keys()

def calcListType(ctype):
    if ctype == "char **" or ctype == "...": return "str"
    isAlist = isList(ctype)
    itemType = None
    isFixed = False
    if isAlist:
        itemType = ctype[:-2]
        if "[" in ctype:
            isFixed=True
            itemType = ctype.split("[")[0].strip()
        return itemType
    return None

def baseType(ctype):
    if isList(ctype): 
        return calcListType(ctype)
    return ctype

aliases={}


def copyfiles(fileList, fromfolder, tofolder):
    for f in fileList:
        shutil.copyfile(fromfolder / f, tofolder / f)

pynames = {
    "from": "from_"
}

def pyname(n):
    if n in pynames.keys(): return pynames[n]
    return n






