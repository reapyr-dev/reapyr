pcmd='python3'
if ! command -v $pcmd &> /dev/null
then
    pcmd = 'python3'
fi
export PYCMD=$pcmd
$pcmd setenv.py > _setvars.sh
chmod +x _setvars.sh
./_setvars.sh

