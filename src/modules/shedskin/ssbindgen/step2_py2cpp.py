import gen_ss_utils as utils
import shutil
import sys

files = ["temp_main.py",  "sstypes.py"] #"FLAGS.reapyr",

def py2cpp():
    sysfile = "FLAGS.reapyr.linux"
    if sys.platform.startswith('win'):
        sysfile = "FLAGS.reapyr.ming"
    elif not sys.platform.startswith('linux'):
        print ("sys.platform was:", sys.platform)
    
    files.append(sysfile)

    utils.copyfiles(files, utils.folder / 'resources', utils.tmp )
    
    sspath = utils.fsroot / "deps" / "shedskin"
    sys.path.append(utils.posix_path(sspath))
    from shedskin import Shedskin
    Shedskin.commandline(["translate", f"--flags={ utils.tmp / sysfile}", f"{utils.tmp / 'temp_main.py'}", ])#f"--outputdir={utils.tmp}"

    shutil.copyfile(utils.tmp / "raylib.cpp", utils.tmp / "raylib.cpp.input")
    