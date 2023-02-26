Reapyr's compiled dependency /assets/ (ie binaries/shared libs/dlls/.a/.dll/.so/etc and headers) will get copied to this folder during the dependancy build process.  Normally they are copied here via a cmake param:

```
cmake -DCMAKE_INSTALL_PREFIX=/path/to/this/folder [otherflags] ..
cmake --build .
cmake --install .
```

These things could also go to some system folder in the future.  For now I'm trying to keep the Reapyr SDK and all its dependancies in a self-contained movable folder for simplicity.  Helps for debugging and helping others that are working through the build process - as I can just ask folks for what landed here, compare files against successful builds, etc.   

Although troubleshooting system include/install folders for multiple platforms is bit more complex, once things stabilize we'll probably move to that model as it's a standard folks expect.
