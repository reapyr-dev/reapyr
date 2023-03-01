Once generated, Shedskin bindings for Raylib containing C++ and Python files get installed in this folder.  The python files that go here give Shedskin the metadata it needs to inference and compile any calling code for those modules, since it doesn't actually know or parse any C++ files, it works purely in Python only, with only C++ at an output step.

During Shedskin invocation the path to this folder is passed as a flag indicating it a lib folder, containing py/cpp/hpp file, Shedskin will understand this and NOT generate C++ for these modules, since it assumes these are hand-written assets that pre-exist, and instead it generates a Makefile to refer to these during C++ compile steps.  (Normally, Shedskin would generate C++ for all python code it encounters.)