#ifndef __SSTYPES_HPP
#define __SSTYPES_HPP

using namespace __shedskin__;
namespace __sstypes__ {

template<class BufferType, class ListType> BufferType* makeBuffer(list<ListType> *data) {
    BufferType* buf = new BufferType[data->units.size()];
    for (int i=0; i<data->units.size(); i++) {
        buf[i] = (BufferType)data->units[i];
    }
    return buf;
}

extern str *const_0;

class VoidPtr;
class SSIntPtr;
class SSFloatPtr;
class SSDoublePtr;
class SSCharPtr;
class SSStrList;

extern str *__name__;

extern class_ *cl_VoidPtr;
class VoidPtr : public pyobj {
public:
    void *ptr=0;

    VoidPtr() {}
    VoidPtr(void* ptr) {
        this->__class__ = cl_VoidPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return ((unsigned char*)ptr)[i];}
    void *__setitem__(__ss_int i, __ss_int val) {((unsigned char*)ptr)[i]=val; return NULL; }
};

extern class_ *cl_SSIntPtr;
class SSIntPtr : public pyobj {
public:
    int *ptr=0;

    SSIntPtr() {}
    SSIntPtr(int* ptr) {
        this->__class__ = cl_SSIntPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(int)val; return NULL; }

    static SSIntPtr *fromList(list<__ss_int> *data) {
        return new SSIntPtr(makeBuffer<int, __ss_int> (data));
    }

};

extern class_ *cl_SSUIntPtr;
class SSUIntPtr : public pyobj {
public:
    unsigned int *ptr=0;

    SSUIntPtr() {}
    SSUIntPtr(unsigned int* ptr) {
        this->__class__ = cl_SSUIntPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(unsigned int)val; return NULL; }
    
    static SSUIntPtr *fromList(list<__ss_int> *data) {
        return new SSUIntPtr(makeBuffer<unsigned int, __ss_int> (data));
    }
};

extern class_ *cl_SSShortPtr;
class SSShortPtr : public pyobj {
public:
    short *ptr=0;

    SSShortPtr() {}
    SSShortPtr(short* ptr) {
        this->__class__ = cl_SSIntPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(short)val; return NULL; }
    
    static SSShortPtr *fromList(list<__ss_int> *data) {
        return new SSShortPtr(makeBuffer<short, __ss_int> (data));
    }
};

extern class_ *cl_SSUShortPtr;
class SSUShortPtr : public pyobj {
public:
    unsigned short *ptr=0;

    SSUShortPtr() {}
    SSUShortPtr(unsigned short* ptr) {
        this->__class__ = cl_SSUShortPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(unsigned short)val; return NULL; }
    
    static SSUShortPtr *fromList(list<__ss_int> *data) {
        return new SSUShortPtr(makeBuffer<unsigned short, __ss_int> (data));
    }
};

extern class_ *cl_SSFloatPtr;
class SSFloatPtr : public pyobj {
public:
    float *ptr=0;

    SSFloatPtr() {}
    SSFloatPtr(float* ptr) {
        this->__class__ = cl_SSFloatPtr;
        this->ptr = ptr;
    }
    __ss_float __getitem__(__ss_int i) { return (__ss_float)ptr[i];}
    void *__setitem__(__ss_int i, __ss_float val) { ptr[i]=(float)val; return NULL; }
        
    static SSFloatPtr *fromList(list<__ss_float> *data) {
        return new SSFloatPtr(makeBuffer<float, __ss_float> (data));
    }
};

SSFloatPtr* makeFloatPtr();// {return new SSFloatPtr(new float[1024]);}

extern class_ *cl_SSDoublePtr;
class SSDoublePtr : public pyobj {
public:
    double *ptr=0;

    SSDoublePtr() {}
    SSDoublePtr(double* ptr) {
        this->__class__ = cl_SSDoublePtr;
        this->ptr = ptr;
    }
    __ss_float __getitem__(__ss_int i)  { return (__ss_float)ptr[i];}
    void *__setitem__(__ss_int i, __ss_float val) { ptr[i]=val; return NULL; }

            
    static SSDoublePtr *fromList(list<__ss_float> *data) {
        return new SSDoublePtr(makeBuffer<double, __ss_float> (data));
    }
};

extern class_ *cl_SSCharPtr;
class SSCharPtr : public pyobj {
public:
    char *ptr=0;

    SSCharPtr() {}
    SSCharPtr(char* ptr) {
        this->__class__ = cl_SSCharPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) {return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(char)val; return NULL; }
            
    static SSCharPtr *fromList(list<__ss_int> *data) {
        return new SSCharPtr(makeBuffer<char, __ss_int> (data));
    }
};

extern class_ *cl_SSUCharPtr;
class SSUCharPtr : public pyobj {
public:
    unsigned char *ptr=0;

    SSUCharPtr() {}
    SSUCharPtr(unsigned char* ptr) {
        this->__class__ = cl_SSUCharPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) {return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(unsigned char)val; return NULL; }
                
    static SSUCharPtr *fromList(list<__ss_int> *data) {
        return new SSUCharPtr(makeBuffer<unsigned char, __ss_int> (data));
    }
};

extern class_ *cl_SSStrList;
class SSStrList : public pyobj {
public:
    char **ptr=0;

    SSStrList() {}
    SSStrList(const char **ptr) {
        this->__class__ = cl_SSStrList;
        this->ptr = (char**)ptr;
    }
    str *__getitem__(__ss_int i) { return new str(ptr[i]); }
    void *__setitem__(__ss_int key, str *val) { 
        char *cstr = new char[val->unit.length() + 1];
        strcpy(cstr, val->unit.c_str());
        ptr[key] = cstr;
        return NULL; 
    }
                    
    static SSStrList *fromList(list<str*> *data) {
        char** buf = new char*[data->units.size()];
        for (int i=0; i<data->units.size(); i++) {
            char *cstr = new char[data->units[i]->unit.length() + 1];
            strcpy(cstr, data->units[i]->c_str());
            buf[i] = cstr;
        }
        return new SSStrList((const char**)buf);
    }
};

void __init();

} // module namespace
#endif
