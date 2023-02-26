#/bin/bash

fullfile=$1
filename=$(basename -- "$fullfile")
filename="${filename%.*}"

echo 'Shedding some skin...'

python -m shedskin translate --flags=${REAPYR_SDK_ROOT}/src/modules/shedskin/ssbindgen/resources/FLAGS.reapyr --outputdir=./build/ $1

make -f ./build/Makefile

./${filename}.exe
