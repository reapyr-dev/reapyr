cd $REAPYR_SDK_ROOT/deps/raylib
mkdir -p build
cd build
cmake -G "MinGW Makefiles" -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release  ..
cmake --build .

mkdir -p $REAPYR_SDK_ROOT/src/modules/cpython/lib/bin/64bit

cp $REAPYR_SDK_ROOT/deps/raylib/build/raylib/libraylib.dll $REAPYR_SDK_ROOT/src/modules/cpython/lib/bin/64bit/raylib.dll

cd $REAPYR_SDK_ROOT/src/modules/cpython/cpygen

python ./headers2json.py
python ./json2cpy.py

cp $REAPYR_SDK_ROOT/src/modules/cpython/cpygen/tmp/raylib.py $REAPYR_SDK_ROOT/src/modules/cpython/lib/

echo $REAPYR_SDK_ROOT
