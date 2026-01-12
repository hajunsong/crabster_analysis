cmake_minimum_required(VERSION 3.16)
project(crm_2025 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Prefer config mode packages (works with most distros too)
find_package(Eigen3 3.3 REQUIRED NO_MODULE)

add_executable(${PROJECT_NAME}
    src/main.cpp
    src/basebody.cpp
    src/subsystem.cpp
    src/simulation.cpp
)

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(${PROJECT_NAME} PRIVATE Eigen3::Eigen)

# Nice warnings (optional)
target_compile_options(${PROJECT_NAME} PRIVATE
    -Wall -Wextra -Wpedantic
)