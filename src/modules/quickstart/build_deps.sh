
# Builds Raylib binaries 
cd $REAPYR_SDK_ROOT/deps/raylib
mkdir -p build
cd build
cmake -G "MinGW Makefiles" -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release  ..
cmake --build .

# Copy Raylib DLL to a folder that CPython ctypes lib will be able to find 
mkdir -p $REAPYR_SDK_ROOT/src/modules/cpython/lib/bin/64bit
cp $REAPYR_SDK_ROOT/deps/raylib/build/raylib/libraylib.dll $REAPYR_SDK_ROOT/src/modules/cpython/lib/bin/64bit/raylib.dll

# Generate CPython code, which uses ctypes lib to invoke Raylib's C APIs from a DLL
cd $REAPYR_SDK_ROOT/src/modules/cpython/cpygen
python ./headers2json.py
python ./json2cpy.py

# Copy the generated ctypes-compliant raylib python module to a folder next to the .dll.  The
# module uses its own file path / location on disk to help find the .dll at runtime, hence the 
# .py and .dll files are located in a folder within close proximity to each other.
cp $REAPYR_SDK_ROOT/src/modules/cpython/cpygen/tmp/raylib.py $REAPYR_SDK_ROOT/src/modules/cpython/lib/

echo "Reapyr dependancy build completed, please inspect scrollback for any errors."
