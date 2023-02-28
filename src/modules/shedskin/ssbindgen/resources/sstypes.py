
class VoidPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass

class SSIntPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSIntPtr()

class SSUIntPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSUIntPtr()

class SSShortPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSShortPtr()

class SSUShortPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSUShortPtr()

class SSFloatPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0.0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSFloatPtr()

class SSDoublePtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0.0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSDoublePtr()

class SSCharPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSCharPtr()

class SSUCharPtr:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return 0
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSUCharPtr()

class SSStrList:
    def __init__(self, ptr=None): self.ptr = None
    def __getitem__(self, i): return ""
    def __setitem__(self, key, val): pass
    @staticmethod
    def fromList(data): return SSStrList()

def makeFloatPtr(): return SSFloatPtr(0.0)

'''
def inferAll():
    tmp1 = SSIntPtr.fromList([0])
    return [
        VoidPtr(0)[0],
        SSIntPtr(0)[0],
        SSFloatPtr(0.0)[0],
        SSDoublePtr(0.0)[0],
        SSCharPtr(0)[0]
    ]
if False: inferAll()
'''