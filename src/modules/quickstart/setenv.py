from pathlib import Path, PurePosixPath
import os
import subprocess

def cmd(c):
    process = subprocess.Popen(c, shell=False)
    process.wait()
    
    return process.returncode

def posix(x):
    return str(PurePosixPath(x)).replace("\\", "")

thisFilePath = Path(os.path.realpath(__file__))
reapyrRoot = thisFilePath.parents[3]

script = f"""
export PYTHONPATH="{posix(reapyrRoot / 'src' / 'modules' / 'cpython' / 'lib')}{os.pathsep}{posix(reapyrRoot / 'deps' / 'shedskin')}"
export PATH=$PATH:"{posix(reapyrRoot / 'src' / 'modules' / 'quickstart')}"
export REAPYR_SDK_ROOT="{posix(reapyrRoot)}"
bash
"""

print (script)
