---
layout: post
title: CMake 学习笔记
data: 2017-11-6 21:38:00
categories: CMake
tags: tools script
---

* content
{:toc}

本文记录了CMake的一些基本的用法和示例, 方便查阅和使用. 

```cmake
cmake_minimum_required(VERSION 3.3)
project(solutionName)
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})
add_executable(projectName main.cpp)
target_link_libraries(projectName ${VTK_LIBRARIES})
```




## Take Care

* CMake 的命令名不区分大小写
* CMake 中的变量通过 `${VARIABLE}` 的格式引用, 要注意是大括号不是小括号(踩了坑...)


## CMakeLists.txt (文件名大小写要正确)

### `cmake_minimum_required`

**格式:** `cmake_minimum_required(VERSION major[.minor[.patch[.tweak]]] [FATAL_ERROR])`

第一个参数 `VERSION` 是关键字, 要大写; 第二个参数为指定的版本号; 第三个参数为可选参数. 如果构建工程使用的 CMake 版本没有达到要求, 配置会被终止, 且显示错误信息. 


### `project`

**格式:** `project(projectName [CXX] [C] [Java])`

该命令指定了解决方案的名称; 可以指定解决方案支持的语言, 语言为可选参数. 默认支持 C/C++. 该命令执行后会产生两个新的变量: `<projectName>_BINARY_DIR` 和 `<projectName>_SOURCE_DIR`. 另外 CMake 预定义了两个变量 `PROJECT_BINARY_DIR` 和 `PROJECT_SOURCE_DIR`, 值和前面两个一致. 另外还有一个自动生成的变量 `PROJECT_NAME` 表示解决方案名称, 可以通过 `${PROJECT_NAME}` 来引用. 

**注意VS中"解决方案"和"项目"的区别.**


### `find_package`

**格式:** `find_package(<package> [version] [EXACT] [QUIET] [MODULE] [REQUIRED] [[COMPONENTS] [components...]] [OPTIONAL_COMPONENTS components...] [NO_POLICY_SCOPE])`

在使用 CMake 构建工程时, 往往会使用外部链接库, 便使用 `find_package` 命令. 我们通过例子来说明.

现在我们想在 CMakeLists 中加入 VTK(Visual ToolKit) 库, 分以下几步:

1. 找到 VTK 库中包含文件 `VTKConfig.cmake` 的路径: `F:\Program Files (x86)\VTK\lib\cmake\vtk-8.0`
2. 然后把该路径加入到用户的环境变量中. 我们令变量名为 `VTK_DIR`, 变量值为 `F:\Program Files (x86)\VTK\lib\cmake\vtk-8.0`.
3. 在 CMakeLists 中使用命令 `FIND PACKAGE(VTK)` 即可.

**注意:** 第2步中的环境变量名必须为 `xyz_DIR` 的格式, 而第3步要查找的模块名称必须是 `xyz`, 即必须和环境变量中的对应.  

| 参数 | 用法 |
|:----:|:-----|
| `version` | 要求包的版本兼容 |
| `EXACT` | 要求包的版本必须严格匹配 |
| `QUIET` | 如果包没找到, 则不显示报错信息 |
| `MODULE` | disables the second signature documented below |
| `REQUIRED` | 如果包没找到, 则会显示出错信息, 并且终止程序 |


### `include`

**格式:** `include(<file|module> [OPTIONAL] [RESULT_VARIABLE <VAR>] [NO_POLICY_SCOPE])`

从给定的文件中加载并运行 CMake 代码. 

| 参数 | 用法 |
|:----:|:-----|
| `OPTIONAL` | 文件不存在时将不会出现错误提示 |
| `RESULT_VARIABLE` | 变量 `<VAR>` 会被设置为完整的文件名, 如果加载失败, 则赋以 `NOTFOUND` |

如果指定了模块而不是文件, 则首先在 `CMAKE_MODULE_PATH` 中搜索名称 `<modulename>.cmake` 的文件, 然后在 CMake 模块目录中搜索. 有一个例外: 如果调用 `include()` 的文件位于 CMake 内置模块目录中, 则首先搜索 CMake 内置模块目录, 然后搜索 `CMAKE_MODULE_PATH`.

参考 `cmake_policy()` 令文档中关于 `NO_POLICY_SCOPE` 选项的讨论.

### `add_executable`

**格式:** `add_executable(<name> [WIN32] [MACOSX_BUNDLE] [EXCLUDE_FROM_ALL] source1 [source2 ...])`

从命令调用中列出的源文件添加一个名为 `<name>` 的可执行目标. `<name>` 对应于逻辑目标名称, 并且在项目中必须是全局唯一的. 构建的可执行文件的实际文件名是基于本地平台(如 `<name>.exe` 或 `<name>`)的约定构建的.

| 参数 | 用法 |
|:----:|:-----|
| `WIN32` | 目标可执行文件会设置 `WIN32_EXECUTABLE` 的属性, 在 Windows 中使用 `WinMain` 作为入口点构建可执行程序 |
| `MACOSX_BUNDLE` | 目标可执行文件会设置 `MACOSX_BUNDLE` 的属性, 构建为 OSX 或 iOS 系统的应用 |
| `EXCLUDE_FROM_ALL` | 从所有的目标中排除该目标 |

`add_executable` 的参数可以使用生成器表达式 `$<...>`, 详细用法参阅 cmake-generator-expression 手册.


### `target_link_libraries`

**格式:** `target_link_libraries(<target> ... <item>... ...)`

<target> 必须已经使用 `add_executable()` 或 `add_library()` 等命令创建. 每一个 `<item>` 可以是:
* 库目标的名称
* 库文件的完整路径
* 一个普通的库名称
