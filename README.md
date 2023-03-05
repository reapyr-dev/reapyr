
![Reapyr](docs/media/reapyrlogo256.png?raw=true "Reapyr")


# Welcome to Reapyr!
## Develop with the simplicity of Python, and the performance of C/C++ !

Reapyr is a set of [Python](https://www.python.org/) bindings for the amazing [Raylib](https://www.raylib.com/) game library. 

It provides both [CPython](https://en.wikipedia.org/wiki/CPython) bindings as well as bindings for [Shedskin](https://shedskin.readthedocs.io/en/latest/) - which is a [transpiler](https://en.wikipedia.org/wiki/Source-to-source_compiler) capable of converting Python code to C++.

Reapyr aims to allow you to write software in Python that will run on as many platforms as possible (including all major desktop and mobile targets), at as close to C/C++ performance as is possible.


# DISCLAIMER: Alpha stuff!

Everything is currently very early dev status - this is purely a volunteer driven project, and we're working to get things stable soon. Feel free to stop over to the [Raylib Python Discord channel](https://discord.com/channels/426912293134270465/661390741104230421) to get live updates as we work, and / or help out!

In the meantime please expect things to probably crash/burn/explode/etc. or plain simply not work yet.  Jump into the Discord for help if you still want to try things out!

# Quickstart

## 1. Check for all Prerequisites

### For Windows:

1. Download and install [w64devkit](https://github.com/skeeto/w64devkit/releases) (click link for download location.)  Most likely on modern PC you'll want the 64 bit version, such as [w64devkit-i686-1.18.0.zip](https://github.com/skeeto/w64devkit/releases/download/v1.18.0/w64devkit-i686-1.18.0.zip). Installing can be as simple as unzipping the .zip file that was downloaded into some folder.

2. Download and install [cmake](https://cmake.org/download/) (click link for download location.) Open the w64devkit shell and ensure the 'cmake' command works before proceeding.  If it doesn't work you may need to add cmake.exe to your Windows system path.

3. Extract the zip from previous step, open a command prompt on your PC, and run the w64devkit.exe file from the install folder. This will drop you into a bash shell. This shell lets you work in a much more portable way. (This shell is much better than the Windows default. It also allows you to work in a way that is maximally compatible with most other major OS's and platforms).

4. Once in a bash shell, go to a suitable folder where you'll download and install the Reapyr SDK. Create a new folder if needed, such as via:  ```mkdir mydevfolder && cd mydevfolder```


### For Linux:
1. If under Linux of course, simply open a shell.
2. Setup cmake, gcc, python3

## 2. Build dependancies and test!

First grab everything from Github, including submodules:
```[bash]
git clone --recurse-submodules https://github.com/reapyr-dev/reapyr.git
```

Run ```setenv.sh``` first, as initializes lots of environment variables that Reapyr's toolset needs.  Then run a script that will Build raylib, bindings, and it copies stuff around so it works at runtime:

```[bash]
cd reapyr/src/modules/quickstart
./setenv
./build_deps
```

Test a CPython example:
```[bash]
cd ../../examples/core/
python ./core_basic_window.py
```
You should see a Raylib window open up with the text: *'You created your first window!'*

Next, run an included script that converts the same example to C++ via Shedskin and runs it:

```[bash]
ssrun ./core_basic_window.py
```

That's it! After the last command you'll see the same result as when run with ```python```, but behind the scenes ```ssrun``` actually converted *all* the code to C++, compiled it, and ran an executable!
