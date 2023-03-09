unameOut="$(uname -s)"
machine="UNKNOWN:${unameOut}"
maketype=""
libext="so"
ibin="lib"
case "${unameOut}" in
    Linux*)     
      machine=Linux
      ;;
    Darwin*)    
      machine=Mac
      ;;
    CYGWIN*)    
      machine=Cygwin
      ;;
    MINGW*)     
      machine=MinGw
      maketype="-G MinGW Makefiles"
      libext="dll"
      ibin="bin"
      ;;
esac

# Build Raylib 

# Before building, this applies a patch to enable raygui if not already enabled
if ! grep -q raygui $REAPYR_SDK_ROOT/deps/raylib/src/CMakelists.txt; then
  cp $REAPYR_SDK_ROOT/deps/raygui/src/raygui.h $REAPYR_SDK_ROOT/deps/raylib/src/
  cd $REAPYR_SDK_ROOT/deps/raylib/src/
  patch < $REAPYR_SDK_ROOT/src/modules/quickstart/resources/useraygui.patch
  echo "Applied patch"
fi

# Setup for cmake
cd $REAPYR_SDK_ROOT/deps/raylib
mkdir -p build
cd build

# Build Raylib shared library (dll/so) here for cpython binding
cmake $maketype -DBUILD_SHARED_LIBS=ON -DBUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$REAPYR_SDK_ROOT/deps/installed ..
cmake --build .
cmake --install .

# 'install' the raygui header
cp $REAPYR_SDK_ROOT/deps/raygui/src/raygui.h $REAPYR_SDK_ROOT/deps/installed/include/

# Build Raylib static library (.a) here for shedskin binding, static linking performance is better
cmake $maketype -DBUILD_SHARED_LIBS=OFF -DBUILD_EXAMPLES=OFF -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$REAPYR_SDK_ROOT/deps/installed ..
cmake --build .
cmake --install .

# Build boehm 
cd $REAPYR_SDK_ROOT/deps/bdwgc
mkdir -p build
cd build
cmake $maketype -Denable_threads=OFF -Denable_cplusplus=ON -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_PREFIX=$REAPYR_SDK_ROOT/deps/installed ..
cmake --build .
cmake --install .

# Build pcre 
cd $REAPYR_SDK_ROOT/deps/libpcre
mkdir -p build
cd build
cmake $maketype -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$REAPYR_SDK_ROOT/deps/installed ..
cmake --build .
cmake --install .

# Copy Raylib DLL to a folder that CPython ctypes lib will be able to find 
mkdir -p $REAPYR_SDK_ROOT/src/modules/cpython/lib/bin/64bit
cp $REAPYR_SDK_ROOT/deps/installed/$ibin/libraylib.$libext $REAPYR_SDK_ROOT/src/modules/cpython/lib/bin/64bit/raylib.$libext

# Generate CPython code, which uses ctypes lib to invoke Raylib's C APIs from a DLL
cd $REAPYR_SDK_ROOT/src/modules/cpython/cpygen
$PYCMD ./headers2json.py
$PYCMD ./json2cpy.py

# Copy the generated ctypes-compliant raylib python module to a folder next to the .dll.  The
# module uses its own file path / location on disk to help find the .dll at runtime, hence the 
# .py and .dll files are located in a folder within close proximity to each other.
cp $REAPYR_SDK_ROOT/src/modules/cpython/cpygen/tmp/raylib.py $REAPYR_SDK_ROOT/src/modules/cpython/lib/

# Next script generates Shedskin bindings, runs a test compile and installs bindings to SS lib folder if successful
cd $REAPYR_SDK_ROOT/src/modules/shedskin/ssbindgen
$PYCMD ./gen_ss_bindings.py

echo "Reapyr dependancy build completed, please inspect scrollback for any errors."
