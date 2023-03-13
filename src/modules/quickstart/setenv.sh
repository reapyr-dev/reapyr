pcmd='python3'
unameOut="$(uname -s)"
case "${unameOut}" in
    Windows_NT*)     
      pcmd='python'
      ;;
    MINGW*)     
      pcmd='python'
      ;;
esac
export PYCMD=$pcmd
$pcmd setenv.py > _setvars.sh
chmod +x _setvars.sh
./_setvars.sh

