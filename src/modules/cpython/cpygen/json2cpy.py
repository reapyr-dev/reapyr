import sys, os

from pathlib import Path, PurePosixPath
filePath = Path(os.path.realpath(__file__))
root = filePath.parents[4]
folder = filePath.parent
tmp = folder / "tmp"

def posix(s): return str(PurePosixPath(s)).replace("\\", "")

sys.path.append(posix(root / "deps" / "raylibpyctbg"))
sys.path.append(posix(root / "deps" / "raylibpyctbg" / "raylibpyctbg"))

from raylibpyctbg import rlapi2

rlapi2.main(
    # inputs to process
    [tmp / 'raylib.h.json', tmp / 'raymath.h.json',  tmp / 'rlgl.h.json'], #tmp / 'raygui.h.json', 
    # output python file to generate
    tmp / 'raylib.py',
    # config file for raylibpyctbg to operate
    root / "deps" / "raylibpyctbg" / "input" / "raylib_api.bind.json"
)
