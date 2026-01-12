### install requirement
```
sudo apt update
sudo apt install -y build-essential cmake
```

### eigen install
```
sudo apt update
sudo apt install libeigen3-dev
```

### build & run
```
mkdir -p build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/eigen_demo
```