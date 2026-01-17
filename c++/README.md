### install requirement
```
sudo apt update
sudo apt install -y build-essential cmake
```

### eigen library
```
mkdir -p third_party
git submodule add https://gitlab.com/libeigen/eigen.git third_party/eigen
git submodule update --init --recursive
```

### python matplotlib
```
sudo apt install python3-dev python3-matplotlib

mkdir -p third_party
cd third_party
git clone https://github.com/lava/matplotlib-cpp.git
```

### build & run
```
mkdir -p build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/crm_2025
```