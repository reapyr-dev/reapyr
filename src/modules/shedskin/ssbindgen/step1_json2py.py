#
# This file is code for 'Step 1' module of the Shedskin binding generation process.
#
# This module loads a JSON file which describes the elements of a C API, and generates a
# Python module that mimics that API.   All structures become classes and all functions 
# become Python methods.  However, no elements actually /do/ anything (the resulting Python
# code is just a shell, it doesn't actually invoke APIs) - they simply contain
# 'cosmetic' markers like 'todo_xyz'.  The purpose of this is for other steps of the 
# binding generation process to look for these markers and swap them out for C++ code that
# actually invokes the real APIs.
#
# This ensures that as the Shedskin compiler evolves, modules generated via these scripts
# will take advantage of any new optimizations in SS's output for any/all bindings automated.
# If one were to genereate the Shedskin C++ code directly, there is a chance in the future that
# Output of this script would fall out of sync with Shedskin's output and cease to be compatible.
#

import gen_ss_utils as utils

'''
# Just for ease of reference, this is schema of the JSON file that raylib parser generates.
# It is the input data for this utility.
{
    'defines':   ['name', 'type', 'value', 'description'],
    'structs':   ['name', 'description', {'fields':['type', 'name', 'description']}],
    'aliases':   ['type', 'name', 'description'],
    'enums':     ['name', 'description', {'values':['name', 'value', 'description']}],
    'callbacks': ['name', 'description', 'returnType', {'params':['type', 'name']}],
    'functions': ['name', 'description', 'returnType', {'params':['type', 'name']}]
}
'''

# Helper to generate accessor for API class setter
def makeSetter(name, type):
    return "\t\tself.{0} = {0}".format(name)

# Converts a C type to value for inferencing via typeValue()
def typeParms(ctype):
    type = utils.calctype(ctype)
    
    if type in utils.defaults.keys(): return utils.defaults[type]

    if type.endswith("List") and type not in utils.defmap.keys():
        subtype = type[:-4]
        if subtype in utils.defmap.keys():
            return typeValue(subtype, False, False)
        return typeValue(subtype.lower(), False, False)

    return ""

# Returns 'default' consts or values for any type. Used to trigger Shedskin inferencing
def typeValue(ctype, apiParam, classParam):
    mapped = utils.maptype(ctype)

    # check if its a pointer type
    if mapped == "list":
        return "{}()".format(utils.ptrType(ctype))

    # check if basic type
    if utils.maptype(ctype) in utils.defaults:
        return "{}".format(typeParms(ctype))
    
    # Probably a custom class type
    if classParam: return "None"
    else: return "{}()".format(utils.maptype(ctype)) # typeParms(ctype)

# Main entrypoint for this module. It will iterate every section
# of the JSON file and generate corresponding Python code.
def gen_ss_py():

    # Loads the JSON describing API we'll analyze
    utils.load_json()

    # Aliases store 'alternate' names for symbols. We'll store these
    # So that if any are encountered we can swap for the 'real' name
    for i in utils.data["aliases"]: 
        utils.aliases[i["name"]] = i["type"] # This is standalone list for reference
        utils.typemap[i["name"]] = i["type"] # This is modifying list of types for conversions

    # Will hold .py output
    output=""

    # Goes to top of output .py file, inits dependant types.
    prologue= """

from sstypes import *

class VoidPointer:
    def __init__(self, val=int(0)):
        self.val = val
"""
    output += prologue

    output += "def todo_create_rlobj(val): pass\n"
    output += "def todo_setter(val): pass\n"
    output += "def todo_getter(val): pass\n"
    output += "def todo_c_implementation_here(val): pass\n"
    output += "def todo_return(val): pass\n"

    for i in utils.data["structs"]:
        output += "todo_{} = 0\n".format((i["name"]))
        output +=  "".join(["todo_{}_{} = 0\n".format(i["name"], j["name"]) for j in i["fields"]])

    #'functions': ['name', 'description', 'returnType', {'params':['type', 'name']}]
    for i in utils.data["functions"]:
        output += "todo_{} = 0\n".format((i["name"]))
        utils.defmap[i["name"]] = i
    
    for i in utils.data["structs"]:
        utils.defmap[i["name"]] = i
        for j in i["fields"]:
            utils.defmap[i["name"]+"_"+j["name"]] = j
        
    for i in utils.data["aliases"]: utils.defmap[i["name"]] = utils.defmap[i["type"]]

    for i in utils.data["structs"]:
        output += "class {}:\n".format(i["name"])

        params = ", ".join(["{} = {}".format(j["name"], typeValue(j["type"], False, True)) for j in i["fields"]])
        
        output += "\tdef __init__(self, {}, rlobj=None):\n".format(params)
        output += "\t\tself.rlobj = rlobj\n\t\tif self.rlobj != None: return\n\t\tself.rlobj = todo_create_rlobj(todo_{})\n".format(i["name"])
        fields = "\n".join([makeSetter(j["name"], j["type"]) for j in i["fields"]])

        output += fields + "\n"
        output += "\t\ttodo_return(0)\n"

        
        getter_fmt = "\t@property\n\tdef {1}(self):\n\t\ttodo_getter(todo_{0}_{1})\n\t\treturn {3}"
        setter_fmt = "\t@{1}.setter\n\tdef {1}(self, val):\n\t\ttodo_setter(todo_{0}_{1} ,val)"

        accessors = "\n".join([getter_fmt.format(i["name"], j["name"], "", typeValue(j["type"], False, False)) + "\n" + setter_fmt.format(i["name"], j["name"], "val")  for j in i["fields"]])

        output += accessors + "\n"
        


    # callbacks: ['name', 'description', 'returnType', 'params':['type', 'name']]
    output += "\n# Callbacks:\n"
    for i in utils.data["callbacks"]:
        output += "class {}:\n".format(i["name"])
        params = ", ".join(["{}: {}".format(j["name"], utils.maptype(j["type"])) for j in i["params"]])
        output += "\tdef invoke(self, {})-> {}: pass\n".format(params, utils.maptype(i["returnType"]))
    output += "\n"

    for i in utils.data["defines"]:
        if i["type"] in ["MACRO", "UNKNOWN"]: continue
        val = i["value"]
        if val == "": val = "1"
        if i["type"] == "STRING": val = '"'+val+'"'
        if i["type"] == "FLOAT_MATH": 
            val = val.replace("f", "")
            if "(" in val or "*" in val or "\\" in val or "+" in val: continue
        if i["type"] == "COLOR": val = val.replace("CLITERAL(Color){", "Color(").replace("}", ")")
        
        output += "{} = {}\n".format(i["name"], val)

    for j in utils.data["enums"]:
        for i in j["values"]:
            output += "{} = {}\n".format(i["name"], i["value"])

    # 'functions': ['name', 'description', 'returnType', 'params':['type', 'name']]
    for i in utils.data["functions"]:
        ret = utils.maptype(i["returnType"])

        outparams = ", ".join(["{}: {}".format(j["name"], utils.maptype(j["type"])) for j in i["params"]]) if "params" in i.keys() else ""
        output += "def {} ({}) -> {}:\n".format(i["name"], outparams,  ret)

        output += '\ttodo_c_implementation_here(todo_{})\n'.format((i["name"]))
        
        if ret == "None":
            output += "\treturn\n"
        else:
            output += "\treturn {}\n".format(typeValue((i["returnType"]), True, False))
        

    output += "\n# Invoke all to force shedskin to generate C++ for them\n"

    output += "def invokeAll():\n"

    #'structs':   ['name', 'description', {'fields':['type', 'name', 'description']}],
    for i in utils.data["structs"]:
        params = ", ".join(["{} = {}".format(j["name"], typeValue(j["type"], True, False)) for j in i["fields"]])
        output += "\ttemp{0} = {0}({1})\n".format(i["name"], params)
        output += "\n".join(["\ttemp{0}_{1}=temp{0}.{1}".format(i["name"], j["name"]) for j in i["fields"]]) + "\n\n"
        output += "\n".join(["\ttemp{0}.{1}={2}".format(i["name"], j["name"], typeValue(j["type"], True, False)) for j in i["fields"]]) + "\n\n"

    output += "\ttempVoidPointer = VoidPointer(1)\n";

    for i in utils.data["functions"]:
        params = ", ".join([typeValue(j["type"], True, False) for j in i["params"]]) if "params" in i.keys() else ""
        output += "\t{}({})\n".format(i["name"], params)

    # All python code has been generated in variable 'output', now it is written to actual Python text file
    import os
    os.system(f"mkdir {utils.tmp}")     # Creates a temp folder to store output
    outfile = utils.tmp / "raylib.py"
    with open(outfile, 'w') as f:
        f.write(output)

    