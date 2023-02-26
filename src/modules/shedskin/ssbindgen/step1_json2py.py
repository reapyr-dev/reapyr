import gen_ss_utils as utils

def makeSetter(name, type):
    #if utils.isList(type):
        #return "\t\tfor i in range(len({0})): self.set_{0}({0}[i], i)".format(name)
        #return "\t\tfor i in range(len({0})): self.set_{0}({0}[i], i)".format(name)
    #return "\t\tself.set_{0}({0})".format(name)
    return "\t\tself.{0} = {0}".format(name)

def typeParms(ctype):
    type = utils.calctype(ctype)
    
    if type in utils.defaults.keys(): return utils.defaults[type]

    if type.endswith("List") and type not in utils.defmap.keys():
        subtype = type[:-4]
        if subtype in utils.defmap.keys():
            return typeValue(subtype, False, False)
        return typeValue(subtype.lower(), False, False)

    return ""

def typeValue(ctype, apiParam, classParam):
    #print ("typeValue:", ctype)
    mapped = utils.maptype(ctype)

    # check if its a pointer type
    if mapped == "list":
        return "{}()".format(utils.ptrType(ctype))

    '''
    if classParam and mapped == "list": 
        return "[]"       
    elif apiParam and mapped == "list": 
        return "[{}]".format( typeParms(ctype))
    '''

    # check if basic type
    if utils.maptype(ctype) in utils.defaults:
        return "{}".format(typeParms(ctype))
    
    # Probably a custom class type
    if classParam: return "None"
    else: return "{}()".format(utils.maptype(ctype)) # typeParms(ctype)

def gen_ss_py():    
    utils.load_json()
    for i in utils.data["aliases"]: 
        utils.aliases[i["name"]] = i["type"]
    #print ("debug:", utils.aliases, utils.maptype("Texture2D"), utils.maptype("Texture2D"), typeValue("Texture2D", True, False))
    #quit()

    
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

    # Will hold .py output
    output=""

    prologue= """

from sstypes import *

class VoidPointer:
    def __init__(self, val=int(0)):
        self.val = val
"""

    for i in utils.data["aliases"]: utils.typemap[i["name"]] = i["type"]

    output += prologue

    for i in utils.data["defines"]:
        if i["type"] in ["MACRO", "UNKNOWN"]: continue
        val = i["value"]
        if val == "": val = "1"
        if i["type"] == "STRING": val = '"'+val+'"'
        if i["type"] == "FLOAT_MATH": 
            val = val.replace("f", "")
            if "(" in val or "*" in val or "\\" in val or "+" in val: continue
        if i["type"] == "COLOR": val = val.replace("CLITERAL(Color){", "[").replace("}", "]")
        
        output += "RL_{} = {}\n".format(i["name"], val)

    for j in utils.data["enums"]:
        for i in j["values"]:
            output += "RL_{} = {}\n".format(i["name"], i["value"])

    output += "def todo_create_rlobj(val): pass\n"
    output += "def todo_setter(val): pass\n"
    output += "def todo_getter(val): pass\n"
    output += "def todo_c_implementation_here(val): pass\n"
    output += "def todo_return(val): pass\n"
    output += "int0 = 0\n"
    output += "float0 = 0.0\n"
    output += "bool0 = False\n"
    output += "str0 = ''\n"
    #output += "emptyList=[]\n"
    for i in utils.data["structs"]:
        output += "todo_{} = 0\n".format((i["name"]))
        output +=  "".join(["todo_{}_{} = 0\n".format(i["name"], j["name"]) for j in i["fields"]])

    #'functions': ['name', 'description', 'returnType', {'params':['type', 'name']}]
    for i in utils.data["functions"]:
        output += "todo_{} = 0\n".format((i["name"]))
        utils.defmap[i["name"]] = i
    #for i in utils.data["aliases"]: utils.typemap[i["name"]] = i["type"]

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
        #setter_fmt = "\tdef set_{1}(self, val, idx=int(0)):\n\t\ttodo_setter(todo_{0}_{1})"
        #getter_fmt = "\tdef get_{1}(self, idx=int(0)):\n\t\ttodo_getter(todo_{0}_{1})\n\t\treturn {3}"
        #print ("*****************************************jtype", i["name"])
        accessors = "\n".join([getter_fmt.format(i["name"], j["name"], "", typeValue(j["type"], False, False)) + "\n" + setter_fmt.format(i["name"], j["name"], "val")  for j in i["fields"]])
        #print ("*****************************************jtype2222", i["name"])
        output += accessors + "\n"
        

        #output += "{}List = list[{}]\n\n".format(i["name"], i["name"])

    #callbacks: ['name', 'description', 'returnType', 'params':['type', 'name']]

    output += "\n# Callbacks:\n"
    for i in utils.data["callbacks"]:
        output += "class {}:\n".format(i["name"])
        params = ", ".join(["{}: {}".format(j["name"], utils.maptype(j["type"])) for j in i["params"]])
        output += "\tdef invoke(self, {})-> {}: pass\n".format(params, utils.maptype(i["returnType"]))
    output += "\n"

    #'functions': ['name', 'description', 'returnType', 'params':['type', 'name']]

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

    import os
    #os.system("mkdir ./tmp/ss")    
    os.system(f"mkdir {utils.tmp}")
    outfile = utils.tmp / "raylib.py"
    #outfile = "D:/dev/vsc_wksp1/raylib-dev01/reapyr/src/examples/hello_reapyr/raylib.py"
    #outfile = './tmp/ss/raylib.py'
    with open(outfile, 'w') as f:
        f.write(output)

    