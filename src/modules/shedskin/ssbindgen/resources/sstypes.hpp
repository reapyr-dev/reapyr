#ifndef __SSTYPES_HPP
#define __SSTYPES_HPP

using namespace __shedskin__;
namespace __sstypes__ {

extern str *const_0;

class VoidPtr;
class SSIntPtr;
class SSFloatPtr;
class SSDoublePtr;
class SSCharPtr;


extern str *__name__;


extern class_ *cl_VoidPtr;
class VoidPtr : public pyobj {
public:
    void *ptr;

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
    int *ptr;

    SSIntPtr() {}
    SSIntPtr(int* ptr) {
        this->__class__ = cl_SSIntPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(int)val; return NULL; }
};

extern class_ *cl_SSUIntPtr;
class SSUIntPtr : public pyobj {
public:
    unsigned int *ptr;

    SSUIntPtr() {}
    SSUIntPtr(unsigned int* ptr) {
        this->__class__ = cl_SSUIntPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(unsigned int)val; return NULL; }
};

extern class_ *cl_SSShortPtr;
class SSShortPtr : public pyobj {
public:
    short *ptr;

    SSShortPtr() {}
    SSShortPtr(short* ptr) {
        this->__class__ = cl_SSIntPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(short)val; return NULL; }
};

extern class_ *cl_SSUShortPtr;
class SSUShortPtr : public pyobj {
public:
    unsigned short *ptr;

    SSUShortPtr() {}
    SSUShortPtr(unsigned short* ptr) {
        this->__class__ = cl_SSUShortPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) { return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(unsigned short)val; return NULL; }
};

extern class_ *cl_SSFloatPtr;
class SSFloatPtr : public pyobj {
public:
    float *ptr;

    SSFloatPtr() {}
    SSFloatPtr(float* ptr) {
        this->__class__ = cl_SSFloatPtr;
        this->ptr = ptr;
    }
    __ss_float __getitem__(__ss_int i) { return (__ss_float)ptr[i];}
    void *__setitem__(__ss_int i, __ss_float val) { ptr[i]=(float)val; return NULL; }
};

SSFloatPtr* makeFloatPtr();// {return new SSFloatPtr(new float[1024]);}

extern class_ *cl_SSDoublePtr;
class SSDoublePtr : public pyobj {
public:
    double *ptr;

    SSDoublePtr() {}
    SSDoublePtr(double* ptr) {
        this->__class__ = cl_SSDoublePtr;
        this->ptr = ptr;
    }
    __ss_float __getitem__(__ss_int i)  { return (__ss_float)ptr[i];}
    void *__setitem__(__ss_int i, __ss_float val) { ptr[i]=val; return NULL; }
};

extern class_ *cl_SSCharPtr;
class SSCharPtr : public pyobj {
public:
    char *ptr;

    SSCharPtr() {}
    SSCharPtr(char* ptr) {
        this->__class__ = cl_SSCharPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) {return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(char)val; return NULL; }
};

extern class_ *cl_SSUCharPtr;
class SSUCharPtr : public pyobj {
public:
    unsigned char *ptr;

    SSUCharPtr() {}
    SSUCharPtr(unsigned char* ptr) {
        this->__class__ = cl_SSUCharPtr;
        this->ptr = ptr;
    }
    __ss_int __getitem__(__ss_int i) {return (__ss_int)ptr[i];}
    void *__setitem__(__ss_int i, __ss_int val) { ptr[i]=(unsigned char)val; return NULL; }
};

void __init();

} // module namespace
#endif
