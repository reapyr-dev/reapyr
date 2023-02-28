# This script isn't executed during the normal binding generation process. It's
# just a helper for binding developers. Steps 1/2 take the most time so we want
# to run them seldomly, so that steps 3/4/5 can be run quickly and repeatedly.  So
# we split into these helper scripts that can be run individually.

import gen_ss_utils as utils

utils.load_json()

print ("Step 3: Modifying C++ files with logic to invoke Raylib APIs...")
import step3_modify_cpp
step3_modify_cpp.modify_ss_cpp()

print ("Step 4: Invoking make and testing the generated Shedskin bindings...")
import step4_build_test
step4_build_test.build_and_test()

print ("Step 5: Installing Shedskin bindings to lib folder...")
import step5_install
step5_install.install_ss_bindings()
