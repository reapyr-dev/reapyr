
class VoidPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

class SSIntPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

class SSUIntPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

class SSShortPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

class SSUShortPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

class SSFloatPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0.0
    def __setitem__(self, key, val): pass

class SSDoublePtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0.0
    def __setitem__(self, key, val): pass

class SSCharPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

class SSUCharPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

def makeFloatPtr(): return SSFloatPtr(0.0)

'''
def inferAll():
    return [
        VoidPtr(0)[0],
        SSIntPtr(0)[0],
        SSFloatPtr(0.0)[0],
        SSDoublePtr(0.0)[0],
        SSCharPtr(0)[0]
    ]
if False: inferAll()

print ("Hello from sstypes.", inferAll())
'''