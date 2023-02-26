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

def load_json():
    global data
    with open(fsroot_modules / "cpython/cpygen/tmp/raylib.h.json") as f:  
        data = json.load(f)

basictypes = ["int", "float", "str", "bool"]

sstypemap = {
    "int":"__ss_int",
    "float":"__ss_float",
    "bool":"__ss_int",# __ss_bool doesnt cast as its a class
}

typemap = {
    "float *": "FloatList",
    "unsigned char *": "IntList",
    "const unsigned char *": "VoidPointer",
    "char *": "str",
    "const char *": "str",
    "char **": "StrList",
    "unsigned short *": "IntList",
    "unsigned int *": "IntList",
    "int *": "IntList",
    "const int *": "IntList",    
    "void *": "VoidPointer",

    "double": "float",
    "unsigned char": "int",
    "unsigned int": "int",
    "unsigned short": "int",
    "rAudioBuffer *": "VoidPointer",
    "rAudioProcessor *": "VoidPointer",
    "void": "None",
    "va_list": "VoidPointer",
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






