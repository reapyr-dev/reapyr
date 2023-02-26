import gen_ss_utils as utils
import shutil
import sys

files = ["temp_main.py", "FLAGS.reapyr", "sstypes.py"]

def py2cpp():
    utils.copyfiles(files, utils.folder / 'resources', utils.tmp )
    
    sspath = utils.fsroot / "deps" / "shedskin"
    sys.path.append(utils.posix_path(sspath))
    from shedskin import Shedskin
    Shedskin.commandline(["translate", f"--flags={ utils.tmp / 'FLAGS.reapyr'}", f"{utils.tmp / 'temp_main.py'}", ])#f"--outputdir={utils.tmp}"

    shutil.copyfile(utils.tmp / "raylib.cpp", utils.tmp / "raylib.cpp.input")
    