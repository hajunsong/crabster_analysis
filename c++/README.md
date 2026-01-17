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

### python matplotlib
```
sudo apt install python3-dev python3-matplotlib
```

### build & run
```
mkdir -p build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/crm_2025
```