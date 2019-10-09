# spinView
GUI for post-processing of spin simulations

## Dependencies
* [NanoGUI](https://github.com/wjakob/nanogui)
* [VFRendering](https://pypi.org/project/pyVFRendering/)
* [OVF parser](https://pypi.org/project/ovf/)


## How to build

While VFRendering and OVF both have Python packages available, nanogui currently
needs to be built and so one can just as well build them all.

```bash
# VFRendering
git clone --recurse-submodules https://github.com/FlorianRhiem/VFRendering
cd VFRendering && mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_PYTHON_BINDINGS=ON
cmake --build . --config Release
cd ../..

# Nanogui
git clone --recurse-submodules https://github.com/wjakob/nanogui
cd nanogui && mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DNANOGUI_BUILD_EXAMPLE=OFF -DNANOGUI_BUILD_SHARED=OFF
cmake --build . --config Release
cd ../..

# OVF
git clone https://github.com/spirit-code/ovf
cd ovf && mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DOVF_BUILD_PYTHON_BINDINGS=ON -DOVF_BUILD_TEST=OFF
cmake --build . --config Release
cd ../..
```