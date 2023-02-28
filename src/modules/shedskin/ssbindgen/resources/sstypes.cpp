#include "builtin.hpp"
#include "sstypes.hpp"

namespace __sstypes__ {

str *const_0;


str *__name__;

class_ *cl_VoidPtr;
class_ *cl_SSIntPtr;
class_ *cl_SSUIntPtr;
class_ *cl_SSShortPtr;
class_ *cl_SSUShortPtr;
class_ *cl_SSFloatPtr;
class_ *cl_SSDoublePtr;
class_ *cl_SSCharPtr;
class_ *cl_SSUCharPtr;
class_ *cl_SSStrList;

SSFloatPtr* makeFloatPtr() {return new SSFloatPtr(new float[1024]);}

void __init() {
    const_0 = new str("Hello from sstypes.");

    __name__ = new str("__main__");

    cl_VoidPtr = new class_("VoidPtr");
    cl_SSIntPtr = new class_("SSIntPtr");
    cl_SSUIntPtr = new class_("SSUIntPtr");
    cl_SSShortPtr = new class_("SSShortPtr");
    cl_SSUShortPtr = new class_("SSUShortPtr");
    cl_SSFloatPtr = new class_("SSFloatPtr");
    cl_SSDoublePtr = new class_("SSDoublePtr");
    cl_SSCharPtr = new class_("SSCharPtr");
    cl_SSUCharPtr = new class_("SSUCharPtr");
    cl_SSStrList = new class_("SSStrList");
    //print(2, NULL, NULL, NULL, const_0, inferAll());
}

} // module namespace
