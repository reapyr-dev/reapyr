import gen_ss_utils as utils

def isBasicType(ctype): return utils.maptype(ctype) in utils.basictypes

def wrapGetType(ctype, val, param):
    #print ("wrapGetType:", ctype, val)
    isBasic = isBasicType(ctype)
    #print ("isBasic:", isBasic)
    isAlist = utils.isList(ctype)
    #print ("isAlist:", isBasic)
    listType = None
    isFixed = False
    if isAlist:
        if "[" in ctype:
            isFixed=True
            listType = ctype.split("[")[0].strip()
        else:
            listType = ctype[:-1].strip()
    
        return wrapGetType(listType, val , param) #+ "[idx]"
    
    if isBasic:
        tmptype = utils.maptype(ctype) 
        if tmptype== "str": return "new str({})".format(val)
        if tmptype== "bool": return "{}?True:False".format(val)
        if param: return "{}".format(val)
        return "({}){}".format(utils.sstypemap [tmptype], val)
    #elif ctype == "void *":
    #    return "new VoidPointer()"#.format(val)

    return formatParam(ctype, val, param)

def formatParam(ctype, val, param):
    if param:
        return "&{}".format(val)
    if ctype == "void **" or ctype == "void *" or utils.maptype(ctype) == "VoidPointer":
        return "new VoidPointer(/*{}*/)".format(val)
    return "new {}(rlobj={})".format(ctype, val)

def typeParam(ctype, param):
    if isBasicType(ctype):
        if ctype.endswith("char *"):
            return "({}){}->c_str()".format(ctype, param)
        return "({}){}".format(ctype, param)
    if not ctype in utils.defmap.keys(): return "NULL"
    elif utils.isList(ctype):
        return "{}".format(param)
    else:
        if not ctype.endswith("*"):
            return "*((rlc::{}*){}->rlobj)".format(ctype, param)
        return "(rlc::{}){}->rlobj".format(ctype, param)

def modify_ss_cpp():

    print("Generating C++...")

    lines=[]
    infile = utils.tmp / "raylib.cpp.input"
    #infile = "D:/dev/vsc_wksp1/raylib-dev01/reapyr/src/examples/hello_reapyr/build/raylib copy.cpp" #raylib copy.cpp
    #infile = './tmp/ss/raylib.cpp'
    with open(infile, 'r') as f:
        lines = f.readlines() 

    output = ""

    skip = 0
    lineIter = iter(lines)
    print (dir(lineIter))
    for line in lineIter:
        if skip > 0:
            skip -=1
            continue
        #output += "\t\ttodo_return(0)\n"
        #this->rlobj = todo_create_rlobj(__raylib__::todo_Vector2);
        if "todo_return(__ss_int(0));" in line: #output += gen_
            
            output += "\treturn NULL;\n".format(objname)
            continue

        if "todo_create_rlobj(__raylib__" in line:
            print ("processing:", line)
            objname = line.split("::todo_")[1].split(")")[0]
            
            output += "\tthis->rlobj = new rlc::{}();\n".format(objname)
            #output += "\tvoid* tmp = new rlc::{}();\n".format(objname)
            continue


        #todo_getter(__raylib__::todo_Vector2_x);
        if "todo_getter(__raylib__" in line:
            print ("processing:", line)
            ids = line.split("::todo_")[1].split(")")[0].split("_")
            objdef = utils.defmap[ids[0]]
            fielddef = utils.defmap[ids[0]+"_"+ids[1]]      
            
            typeVal = "((rlc::{}*)this->rlobj)->{}".format(objdef["name"], fielddef["name"])

            if fielddef["type"] in ["char **", "float[2]"]: continue
            #output += "\treturn ({});\n".format(wrapGetType(fielddef["type"], typeVal))
            nextLine = next(lineIter)
            if not "NULL" in nextLine: 
                output += "\treturn {};\n".format(wrapGetType(fielddef["type"], typeVal, False))
            else:
                output += nextLine.replace("NULL)", wrapGetType(fielddef["type"], typeVal, True)+ ")") 
            #skip = 1
            continue
        #todo_setter(__raylib__::todo_Ray_position);
        if "todo_setter(__raylib__" in line:
            ids = line.split("::todo_")[1].split(")")[0].split("_")
            objdef = utils.defmap[ids[0]]
            fielddef = utils.defmap[ids[0]+"_"+ids[1]]
            suffix = ""
            #if utils.isList(fielddef["type"]):
            #    suffix = "[idx]"
            #bt = utils.baseType(fielddef["type"])
            bt = fielddef["type"]
            mt = utils.maptype(utils.baseType(fielddef["type"]))
            output += "\t// debug:" + str([fielddef["type"], isBasicType(bt), bt, mt]) + "\n"
            casttype = fielddef["type"]
            if utils.isList(fielddef["type"]) and casttype.endswith("*"): casttype = casttype[0:-1].strip()
            castsuffix=""
            if "[" in casttype: casttype = casttype.split("[")[0].strip()
            if bt in ["char **", "float[2]", "Matrix[2]", "float[4]", "Transform **", "void *"]: continue
            if isBasicType(bt) or mt == "VoidPointer":
                #fielddef["type"]
                output += "\t// debug:" + str(["case1"]) + "\n"
                cast = "({})".format(casttype)
                valsuffix = ""

                if mt == "str" and "[" in fielddef["type"]:
                    output += "\trlconvertStringFixed(val, ((rlc::{0}*)this->rlobj)->{1}{2});\n".format(objdef["name"], fielddef["name"], suffix)
                    continue

                if bt == "str":
                    valsuffix = "->unit.c_str()"
                    cast = "(char*)"
                
                if mt == "VoidPointer":
                    valsuffix = "->val"
                    if fielddef["type"] == "void *":
                        cast = "(void *)"
                    else:
                        cast = "(rlc::"+fielddef["type"]+")"

                output += "\t((rlc::{0}*)this->rlobj)->{1}{3} = {2}val{4};\n".format(objdef["name"], fielddef["name"], cast, suffix, valsuffix)
            else:
                output += "\t// debug:" + str(["case2"]) + "\n"
                if casttype.endswith("**"): casttype = casttype[0:-1]
                cast=""
                if utils.isList(fielddef["type"]) and isBasicType(utils.baseType(fielddef["type"])):
                    output += "\t// debug:" + str(["case2.2 hmm"]) + "\n"
                    cast = "({})val->ptr".format(fielddef["type"])
                else:
                    cast = "(rlc::{})val->rlobj".format(fielddef["type"])
                    if not fielddef["type"].strip().endswith("*"):
                        output += "\t// debug:" + str(["case2.3", casttype]) + "\n"
                        cast = "*((rlc::{}*)val->rlobj)".format(casttype)
                output += "\t((rlc::{0}*)this->rlobj)->{1}{3} = {2};\n".format(objdef["name"], fielddef["name"], cast, suffix)
            continue
        
        #todo_c_implementation_here(__raylib__::todo_GetGestureDragVector);
        #return (new Vector2(default_1, default_2, NULL));

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
            output += "\t//Debug: "+ str([funcdef]) + "\n"
            output += "\t//Debug: "+ str([rt, utils.maptype(rt), utils.calctype(rt)]) + "\n"
            if rt in [ "char **", "const char **"]: doSkip = True
            if "params" in funcdef.keys():
                for j in funcdef["params"]:
                    if j["type"] in ["...", "char **"]: doSkip=True
            if doSkip:
                #nextLine = next(lineIter)
                #output += "\treturn NULL;\n"
                #output += nextLine
                continue
            else:
                suffix = ""
                if rt != "void":
                    if isBasicType(rt) or (utils.isList(rt) and isBasicType(utils.baseType(rt))) or rt=="void *":
                        ret = "{} result = ".format(rt)
                        if rt == "bool": suffix = "?True:False"
                    else:
                        ret = "rlc::{0}* result = new rlc::{0}(); *result = ".format(rt)
                
                params = ", ".join([typeParam(j["type"], j["name"]) for j in funcdef["params"]]) if "params" in funcdef.keys() else ""
                callfunc = "\t{}rlc::{}({}){};\n".format(ret, func, params, "")                

                output += callfunc
                if rt != "void":
                    nextLine = next(lineIter)
                    if not "NULL" in nextLine:
                        if utils.maptype(rt) == "str":
                            output += "\treturn new str(result);\n"
                        elif rt=="void *":
                            output += "\treturn new VoidPointer(/*result*/);\n"
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
    #outfile = "D:/dev/vsc_wksp1/raylib-dev01/reapyr/src/examples/hello_reapyr/build/raylib.cpp"
    #outfile = "./tmp/ss/raylib.cpp.modified"
    with open(outfile, 'w') as f:
        f.write(output)

    #print (maptype("char **"))
    #print (baseType("char **"))

def gen_prologue(line):
    output = ""
    if line.strip() == '#include "raylib.hpp"':
        output += """

namespace rlc {
    #include <raylib.h>
}
            """
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

list<__ss_float> * convertList (float * buffer) {
    return new list<__ss_float>;
}

"""    
    return output