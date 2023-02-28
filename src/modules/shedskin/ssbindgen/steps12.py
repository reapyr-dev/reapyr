# This script isn't executed during the normal binding generation process. It's
# just a helper for binding developers. Steps 1/2 take the most time so we want
# to run them seldomly, so that steps 3/4/5 can be run quickly and repeatedly.  So
# we split into these helper scripts that can be run individually.

print ("Step 1: Generating raylib.py from JSON files in this repo....")
import step1_json2py
step1_json2py.gen_ss_py()

print ("Step 2: Invoking Shedskin on raylib.py to generate stub C++ code...")
import step2_py2cpp
step2_py2cpp.py2cpp()