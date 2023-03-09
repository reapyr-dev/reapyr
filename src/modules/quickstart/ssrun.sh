#/bin/bash

unameOut="$(uname -s)"
mext=".linux"
bext=""
case "${unameOut}" in
    MINGW*)     
      mext=".mingw"
      bext=".exe"
      ;;
esac


fullfile=$1
filename=$(basename -- "$fullfile")
filename="${filename%.*}"

echo 'Shedding some skin...'

$PYCMD -m shedskin translate --flags=${REAPYR_SDK_ROOT}/src/modules/shedskin/ssbindgen/resources/FLAGS.reapyr$mext --outputdir=./build/ $1

make -f ./build/Makefile
bin="$filename$bext"
./${bin}
