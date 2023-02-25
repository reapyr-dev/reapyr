
![Reapyr](docs/media/reapyrlogo256.png?raw=true "Reapyr")


# Reapyr: Develop with the simplicity of Python, and the performance of C/C++ !

Reapyr is a set of [Python](https://www.python.org/) bindings for the amazing [Raylib](https://www.raylib.com/) game library. 

It provides both [CPython](https://en.wikipedia.org/wiki/CPython) bindings as well as bindings for [Shedskin](https://shedskin.readthedocs.io/en/latest/) - which is a [transpiler](https://en.wikipedia.org/wiki/Source-to-source_compiler) capable of converting Python code to C++.

Reapyr aims to run on as many platforms as possible - including desktop and mobile targets.


# Note: Alpha disclaimer!

Stuff is currently very early dev status - this is purely a volunteer driven project, and we're working to get things stable soon. Feel free to stop over to the [Raylib Python Discord channel](https://discord.com/channels/426912293134270465/661390741104230421) to get live updates as we work, and / or help out!

# Quickstart

## 1. Check for all Prerequisites

### For Windows:

1. Download and install [w64devkit](https://github.com/skeeto/w64devkit/releases) (click link for download location.)  Most likely on modern PC you'll want the 64 bit version, such as [w64devkit-i686-1.18.0.zip](https://github.com/skeeto/w64devkit/releases/download/v1.18.0/w64devkit-i686-1.18.0.zip)

2. Extract the zip from previous step, an open a command prompt on your PC, and run the w64devkit.exe file from install folder. This will drop you into a bash shell, this lets you work in a much more portable way. 

3. Once in a bash shell, go to a suitable folder where you'll download and install the Reapyr SDK. Create a new if needed, such as via:  ```mkdir mydevfolder && cd mydevfolder```


### For Linux:
1. If under Linux of course, simply open a shell.
2. Setup cmake, gcc, python3

## 2. Build dependancies and test!

First grab everything from Github, including submodules:
```[bash]
git clone --recurse-submodules https://github.com/reapyr-dev/reapyr.git
```

Run a script that will Build raylib, bindings, and it copies stuff around so it works at runtime:

```[bash]
cd reapyr/src/modules/quickstart
./setenv
./build_deps
```

Test a CPython example:
```[bash]
cd ../../examples/raylib/hello_raylib/
```
You should see a Raylib window open up with the text: *'You created your first window!'*

Next, run an included script that converts the same example to C++ via Shedskin and run it:

```[bash]
# *** STAY TUNED: COMING SOON! ***
```