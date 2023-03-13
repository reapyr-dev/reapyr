import os

class ast:
    def __init__(self, children=[], params=[], line=0):
        self.children = children
        self.params = params
        self.line = line
    
    def expand(self, flags, nest):
        return "".join([i.expand(flags, nest+1) for i in self.children])

    def dump(self, nest=0):
        ret =  ("\t"* nest) + self.__class__.__name__ + "\n"
        for i in self.children:
            ret += i.dump(nest+1)
        return ret

class ifdef(ast):
    def evaluate(self, flags):
        func = self.params[0].strip()
        negate = False
        if func == "#ifndef": negate=True
        key = self.params[1].strip()
        test = key in flags.keys() and flags[key] != ""
        if negate: return not test
        return test
    
    def expand(self, flags, nest):
        result = ""
        
        if self.evaluate(flags):#
            for i in self.children:
                child = i.expand(flags, nest+1)
                if child.strip().split(" ")[0].strip() != "#endif":
                    result += child
        return result

class text(ast):
    def expand(self, flags, nest): return self.params[0]

class Preprocessor():
    def __init__(self, flags):
        self.index = 0
        self.flags = flags

    def preprocessLine(self, lines, parent):
        
        if self.index >= len(lines): 
            self.index = -1
            return text(line=-1, params=[""])

        line = lines[self.index]

        directive = None
        if line.strip().startswith("#"):
            directive = line.strip().split(" ")
            if directive[0].strip() in ["#ifdef", "#ifndef", "#if"]:
                self.index += 1
                newparent = ifdef(params=directive, line=self.index, children=[])
                parent.children.append(newparent)
                self.preprocessLines(lines, newparent)
                return newparent
        
        self.index += 1

        result = text(line=self.index, params=[line])

        parent.children.append(result)
        return result

    def preprocessLines(self, lines, parent):
        while self.index >= 0:
            item = self.preprocessLine(lines, parent)
            if item.line == -1 or item.params[0].strip() == "#endif" or item.params[0].split(" ")[0] == "#endif":
                return

    def preprocessFile(self, f):
        print ("Preprocessing file:", f)
        file = open(f, 'r')
        lines = file.readlines()
        self.index = 0
        result = ast(children=[])
        self.preprocessLines(lines, result)
        if self.index < len(lines) and self.index >=0: raise Exception("error parsing, failed at: " + str(self.index))
        return result.expand(self.flags, 0)#self.expand(result.children)

from pathlib import Path
filePath = Path(os.path.realpath(__file__))
root = filePath.parents[4]
folder = filePath.parent
tmp = folder / "tmp"

headers = [
    root / f"deps/raylib/src/raylib.h",
    root / f"deps/raylib/src/raymath.h",
    root / f"deps/raygui/src/raygui.h",
    root / f"deps/raylib/src/rlgl.h"
]

params = [
    "-d RLAPI",
    "-d RMAPI",
    "-d RAYGUIAPI",
    "-d RLAPI",
]

def preprocess():
    os.system(f"mkdir {tmp}")
    for i in headers:
        output =  Preprocessor({}).preprocessFile(i)
        print (output)
        outHeader = tmp / f"{i.name}.preprocessed"
        open(outHeader, "w").write(output)

def runparser():    
    os.system(f"gcc {root/'deps/raylib/parser/raylib_parser.c'}")
    binary = "a.out"
    if Path(folder / "a.exe").is_file(): binary = "a.exe"
    idx = 0
    for i in headers:
        out_header = tmp / f"{i.name}.preprocessed"
        out_json = tmp / f"{i.name}.json"
        os.system(f"{folder / binary} --input {out_header} --output {out_json} --format JSON {params[idx]}")
        idx += 1

preprocess()
runparser()