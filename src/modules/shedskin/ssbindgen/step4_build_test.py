import gen_ss_utils as utils
import subprocess
import sys
from pathlib import Path

files_sstypes = ["sstypes.cpp", "sstypes.hpp"]

def cmd(c, data=None):
    if data != None:
        process = subprocess.Popen(c,shell=False, stdout=subprocess.PIPE)
        result=""
        while process.poll() is None:
            for ch in iter(lambda: process.stdout.read(1), b""):
                sys.stdout.buffer.write(ch)
                result+=str(ch.decode("utf-8"))
        data.append(result)
        return process.returncode
    else:
        process = subprocess.Popen(c.split(" "), shell=False)
        process.wait()
        
        return process.returncode

def build_and_test():
    utils.copyfiles(files_sstypes, utils.folder / 'resources', utils.tmp )    
       
    if cmd(f"make -f {utils.tmp / 'Makefile'}") != 0: # Success 0 else not
        print("Error detected during make. Please correct and rerun this script.")
        quit()
        return False

    data=[]
    binary = "temp_main"
    if Path(utils.tmp / "temp_main.exe").is_file(): binary = "temp_main.exe"
    testresult = cmd(f"{utils.tmp / binary}", data=data)
    print ("Exec result:", testresult, data)
    if testresult==0 and len(data) ==1 and data[0].strip() == "OK":
        return True
    print("Test of Shedskin bindings failed. Please fix and rerun script.")
    quit()
    return False

if __name__ == "__main__": build_and_test()