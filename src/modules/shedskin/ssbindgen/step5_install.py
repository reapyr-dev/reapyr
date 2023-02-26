import gen_ss_utils as utils

files_generated = ["sstypes.py", "sstypes.cpp", "sstypes.hpp", "raylib.py", "raylib.cpp", "raylib.hpp"]

def install_ss_bindings():
    # this is where files should go, but after recent Shedskin changes external lib
    # dir seems broke. this needs debugging
    # destinationPath = utils.fsroot / "src" / "modules" / "shedskin" / "lib" 

    # So instead we'll toss things into the Shedskin base lib folder
    destinationPath = utils.fsroot / "deps" / "shedskin" / "shedskin" / "lib" 
    utils.copyfiles(files_generated, utils.tmp,  destinationPath )    
    print (f"Shed skin bindings have been copied from {utils.tmp} to {destinationPath}")