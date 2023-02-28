import gen_ss_utils as utils

# Helper method to see if a type is basic (int, double, etc.)
def isBasicType(ctype): return utils.maptype(ctype) in utils.basictypes

typeOverrides = {
    "char **": ["SStrList", "const char **"],
    "const char **": ["SStrList", "const char **"]
}

# Generates code executed when 'getting' a property member of a Struct type
# We use python getter decorators to simulate property access although it's 
# actually a method being called.
def wrapGetType(ctype, val, param):

    if param and ctype in typeOverrides.keys():
        return "({}){}".format(typeOverrides[ctype][1], val)
    
    isBasic = isBasicType(ctype)
    isAlist = utils.isList(ctype)
    listType = None
    isFixed = False
    if isAlist:
        if "[" in ctype:
            isFixed=True
            listType = ctype.split("[")[0].strip()
        else:
            listType = ctype[:-1].strip()
    
        return wrapGetType(listType, val , param)
    
    if isBasic:
        tmptype = utils.maptype(ctype) 
        if tmptype== "str": return "new str({})".format(val)
        if tmptype== "bool": return "{}?True:False".format(val)
        if param: return "{}".format(val)
        return "({}){}".format(utils.sstypemap [tmptype], val)
    #elif ctype == "void *":
    #    return "new VoidPointer()"#.format(val)

    return formatParam(ctype, val, param)

# Wraps a value returned from a getter method, to convert it from native C type into
# SS type
def formatParam(ctype, val, param):
    if param:
        return "&{}".format(val)
    if ctype == "void **" or ctype == "void *" or utils.maptype(ctype) == "VoidPtr":
        return "new VoidPtr({})".format(val)
    return "new {}(rlobj={})".format(ctype, val)

# This converts a SS type into a native C type so that it can be passed into function call param.
def typeParam(ctype, param):
    if isBasicType(ctype):
        if ctype.endswith("char *"):
            return "({}){}->c_str()".format(ctype, param)
        if ctype == "char":
            return "({}){}->c_str()[0]".format(ctype, param)
        if ctype == "...":
            return "{}->c_str()".format(param)
        return "({}){}".format(ctype, param)
    usetype = ctype
    if usetype.startswith("const"):
        usetype = usetype[6:]
    if utils.isList(usetype) and not usetype in utils.defmap.keys():
        if usetype.endswith("**"): usetype=usetype[:-1]
        if utils.baseType(usetype) in utils.defmap.keys():
            if ctype.startswith("const"):
                return "(const rlc::{}){}->rlobj".format(ctype[6:], param)
            
            return "(rlc::{}){}->rlobj".format(ctype, param)
        return "({}){}->ptr".format(ctype, param)
    elif not usetype in utils.defmap.keys(): 
        return "NULL"
    else:
        if not usetype.endswith("*"):
            return "*((rlc::{}*){}->rlobj)".format(usetype, param)
        return "(rlc::{}){}->rlobj".format(usetype, param)
    

# debug helpers here, types get inserted into these lists to bypass them, for situations where
# big refactoring is happening and needing to reduce API surface for testing while working
skiptypes_getter = [] 
skiptypes_setter = []
skiptypes_returned = []
skiptypes_params = []

# Enables debugging markers to appear in generated code to help troubleshoot patterns
ENABLE_DEBUG_STRS=True
def DEBUG_STR(s):
    if ENABLE_DEBUG_STRS: return s
    return ""

# Main entry point for this step.  What this method does is input a C++ file generated
# from Shedskin that contains a bunch of 'nonfunctional' markers named like 'todo_xyz'.
# Line by line we read the .cpp file, look for these markers and swap them for actual C++
# code that invokes the functionality needed to access the 'real' API being wrapped.
def modify_ss_cpp():

    print("Generating C++...")

    lines=[]

    # We work from a temp file, so always starting from
    # pristine input, making this step repeatable for debugging
    infile = utils.tmp / "raylib.cpp.input"  

    with open(infile, 'r') as f:
        lines = f.readlines() 

    output = ""

    skip = 0
    lineIter = iter(lines)

    for line in lineIter:
        if skip > 0: # skip counter to remove N lines from output
            skip -= 1
            continue        

        if "todo_return(__ss_int(0));" in line:            
            output += "\treturn NULL;\n".format(objname)
            continue

        # Example line: this->rlobj = todo_create_rlobj(__raylib__::todo_Vector2);
        if "todo_create_rlobj(__raylib__" in line:
            print ("processing:", line)
            objname = line.split("::todo_")[1].split(")")[0]            
            output += "\tthis->rlobj = new rlc::{}();\n".format(objname)
            continue

        # Example line: todo_getter(__raylib__::todo_Vector2_x);
        if "todo_getter(__raylib__" in line:
            print ("processing:", line)
            ids = line.split("::todo_")[1].split(")")[0].split("_")
            objdef = utils.defmap[ids[0]]
            fielddef = utils.defmap[ids[0]+"_"+ids[1]]      
            
            typeVal = "((rlc::{}*)this->rlobj)->{}".format(objdef["name"], fielddef["name"])

            if fielddef["type"] in skiptypes_getter: continue

            nextLine = next(lineIter)
            if not "NULL" in nextLine: 
                output += "\treturn {};\n".format(wrapGetType(fielddef["type"], typeVal, False))
            else:
                output += nextLine.replace("NULL)", wrapGetType(fielddef["type"], typeVal, True)+ ")") 

            continue

        # Example line: todo_setter(__raylib__::todo_Ray_position);
        if "todo_setter(__raylib__" in line:
            ids = line.split("::todo_")[1].split(")")[0].split("_")
            objdef = utils.defmap[ids[0]]
            fielddef = utils.defmap[ids[0]+"_"+ids[1]]
            suffix = ""

            bt = fielddef["type"]
            mt = utils.maptype(utils.baseType(fielddef["type"]))
            output += DEBUG_STR("\t// debug:" + str([fielddef["type"], isBasicType(bt), bt, mt]) + "\n")
            casttype = fielddef["type"]
            if utils.isList(fielddef["type"]) and casttype.endswith("*"): casttype = casttype[0:-1].strip()
            castsuffix=""
            if "[" in casttype: casttype = casttype.split("[")[0].strip()
            if bt in skiptypes_setter: continue

            if isBasicType(bt) or mt == "VoidPtr":
                output += DEBUG_STR("\t// debug:" + str(["case1"]) + "\n")
                cast = "({})".format(casttype)
                valsuffix = ""

                if mt == "str" and "[" in fielddef["type"]:
                    output += "\trlconvertStringFixed(val, ((rlc::{0}*)this->rlobj)->{1}{2});\n".format(objdef["name"], fielddef["name"], suffix)
                    continue
                

                if bt in typeOverrides.keys():
                    valsuffix = "->ptr"
                    cast = "({})".format(bt)
                elif bt == "str":
                    valsuffix = "->unit.c_str()"
                    cast = "(char*)"
                
                if mt == "VoidPtr":
                    valsuffix = "->ptr"
                    if fielddef["type"] == "void *":
                        cast = "(void *)"
                    else:
                        cast = "(rlc::"+fielddef["type"]+")"

                output += "\t((rlc::{0}*)this->rlobj)->{1}{3} = {2}val{4};\n".format(objdef["name"], fielddef["name"], cast, suffix, valsuffix)
            else:
                output += DEBUG_STR("\t// debug:" + str(["case2"]) + "\n")
                if casttype.endswith("**"): casttype = casttype[0:-1]
                cast=""
                if utils.isList(fielddef["type"]) and isBasicType(utils.baseType(fielddef["type"])):
                    output += DEBUG_STR("\t// debug:" + str(["case2.2 hmm"]) + "\n")
                    if "[" in fielddef["type"]:
                        ct = fielddef["type"].split("[")[0]
                        listSize = int(fielddef["type"].split("[")[1][:-1])
                        output += "\tconvertListFixed<{3}>(val->ptr, ((rlc::{0}*)this->rlobj)->{1}{2}, {4});\n".format(objdef["name"], fielddef["name"], suffix, ct, listSize)
                        continue
                    cast = "({})val->ptr".format(fielddef["type"])
                else:
                    cast = "(rlc::{})val->rlobj".format(fielddef["type"])
                    if not fielddef["type"].strip().endswith("*"):
                        output += DEBUG_STR("\t// debug:" + str(["case2.3", casttype]) + "\n")
                        cast = "*((rlc::{}*)val->rlobj)".format(casttype)
                    if "[" in fielddef["type"]:
                        base = utils.baseType(fielddef["type"])
                        ct = fielddef["type"].split("[")[0]
                        listSize = int(fielddef["type"].split("[")[1][:-1])
                        output += "\tconvertListFixed<rlc::{3}>((rlc::{3}*)val->rlobj, ((rlc::{0}*)this->rlobj)->{1}{2}, {4});\n".format(objdef["name"], fielddef["name"], suffix, ct, listSize)
                        continue

                output += "\t((rlc::{0}*)this->rlobj)->{1}{3} = {2};\n".format(objdef["name"], fielddef["name"], cast, suffix)
            continue
        
        if "todo_c_implementation_here(__raylib__" in line:
            func = line.split("::todo_")[1].split(")")[0].strip()
            funcdef = utils.defmap[func]
            #    'functions': ['name', 'description', 'returnType', {'params':['type', 'name']}]
            ret = ""
            retobj = ""
            rt = funcdef["returnType"]
            doSkip = False
            '''if "params" in funcdef.keys():
                for j in funcdef["params"]: 
                    if not isBasicType(j["type"]) and j["type"] not in utils.defmap.keys(): 
                        output += "\t//skipping due to param " + j["name"] + " having unsupported type " + j["type"] + "\n"
                        doSkip=True
            '''
            output += DEBUG_STR("\t//Debug: "+ str([funcdef]) + "\n")
            output += DEBUG_STR("\t//Debug: "+ str([rt, utils.maptype(rt), utils.calctype(rt)]) + "\n")

            if rt in skiptypes_returned : doSkip = True

            if "params" in funcdef.keys():
                for j in funcdef["params"]:
                    if j["type"] in skiptypes_params: doSkip=True

            if doSkip:
                continue
            else:
                suffix = ""
                if rt != "void":
                    if isBasicType(rt) or (utils.isList(rt) and isBasicType(utils.baseType(rt))) or rt=="void *":
                        ret = "{} result = ".format(rt)
                        if rt == "bool": suffix = "?True:False"
                    else:
                        ret = "rlc::{0}* result = new rlc::{0}(); *result = ".format(rt)
                
                params = ", ".join([typeParam(j["type"], utils.pyname(j["name"])) for j in funcdef["params"]]) if "params" in funcdef.keys() else ""
                callfunc = "\t{}rlc::{}({}){};\n".format(ret, func, params, "")                

                output += callfunc
                if rt != "void":
                    nextLine = next(lineIter)
                    if not "NULL" in nextLine:
                        if utils.maptype(rt) == "str":
                            output += "\treturn new str(result);\n"
                        elif rt=="void *":
                            output += "\treturn new VoidPtr(result);\n"
                        elif utils.isList(rt):
                            output += "\treturn convertList(result);\n"
                        else:
                            output += "\treturn result{};\n".format(suffix)
                    else:
                        cast = ""
                        if isBasicType(rt):
                            cast = "({})".format(rt)
                        output += nextLine.replace("NULL)", "{}result)".format(cast))
                continue

        output += line

        output += gen_prologue(line)

    outfile = utils.tmp / "raylib.cpp"

    with open(outfile, 'w') as f:
        f.write(output)

def gen_prologue(line):
    output = ""
    if line.strip() == '#include "raylib.hpp"':
        output += """

namespace rlc {
    #include <raylib.h>
    #include <raymath.h>
    #include <rlgl.h>
    #include <raygui.h>
}
            """
        # Have to undefine C globals or they clash with
        # Generated equivalents. Gotta love C and global
        # namespaces!
        for i in utils.data["defines"]:
            output += f"#undef {i['name']}\n"
        
    elif line.strip() == "namespace __raylib__ {":
        output += """

char* rlconvertStringFixed(str* input, char* output) {
    int n = input->unit.length();
    for (int i = 0; i < n; i++) {
        output[i] = input->unit[i];
    }
    output[n]=0;
    return output;
}

template <class T> void convertListFixed(T* input, T* output, int size) {
    for (int i = 0; i < size; i++)
        output[i] = input[i];
}

list<__ss_float> * convertList (float * buffer) {
    return new list<__ss_float>;
}

"""    
    return output