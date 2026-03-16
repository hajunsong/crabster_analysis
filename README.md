### install requirement
```
sudo apt update
sudo apt install -y build-essential cmake
```

### eigen library
```
sudo apt-get install libeigen3-dev
```

### build & run
```
mkdir -p build
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
./build/crm_2025
```

### plot
```
sudo apt-get install python3 python3-dev python3-pip
sudo apt-get install python3-numpy python3-pandas python3-matplotlib
```