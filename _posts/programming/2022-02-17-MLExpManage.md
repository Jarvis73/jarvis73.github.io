---
layout: post
title: "MongoDB + Omniboard 实验管理"
date: 2022-02-17 16:27:00 +0800
categories: Framework
author: Jarvis
meta: Post
pin: True
---

* content
{:toc}

本文面向机器学习工作者, 使用 Sacred 库来管理实验: MongoDB 存储实验数据, Omniboard 可视化数据库.

我们前面已经介绍过在机器学习实验中如何使用 Sacred (见 [Sacred 教程](/2020/11/15/Sacred/)), 这里我们将介绍如何使用 MongoDB 对 Sacred 进行实验管理, 并使用 Omniboard 可视化实验信息. 



本文提供两种方法来安装 MongoDB 和 Omniboard 库.
* 使用Docker (推荐, 但需要服务器上有 docker, 并且当前用户在 docker 用户组里.)
* 手动安装

## 1. MongoDB

> MongoDB 是由C++语言编写的, 是一个基于分布式文件存储的开源数据库系统. 在高负载的情况下, 添加更多的节点, 可以保证服务器性能. MongoDB 旨在为WEB应用提供可扩展的高性能数据存储解决方案. MongoDB 将数据存储为一个文档, 数据结构由键值(key=>value)对组成. MongoDB 文档类似于 JSON 对象. 字段值可以包含其他文档，数组及文档数组.    ---- [MongoDB 简介](https://www.runoob.com/mongodb/mongodb-intro.html))

### 1.1 使用 Docker 安装

拉取镜像, 并创建一个网络.

```bash
# 拉取镜像
docker pull mongo:4.4.4

# 创建网络 (用于后续 Omniboard 的 docker 连接到该 docker)
docker network create sacred
```

开启容器, 把端口容器内的 27017 (MongoDB 默认端口) 映射到 host 的 7000 (可自定) 端口, 把容器内的 `/data/db` 映射到 host 的 `/path/to/db` (可自定).

```bash
docker run -p 7000:27017 -v /path/to/db:/data/db --name sacred_mongo --network sacred -d mongo:4.4.4
```

### 1.2 手动安装

* 如果拥有系统管理员权限, 则可以直接使用包管理工具安装.
* 如果没有管理员权限 则可以从 [MongoDB 官网](https://www.mongodb.com/try/download/community) 下载独立安装包, 选择合适的系统和版本, 下载 tgz 文件, 解压, 并拷贝到自定义目录. 

  ```bash
  curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2004-4.4.4.tgz

  tar -zxvf mongodb-linux-x86_64-ubuntu2004-4.4.4.tgz

  mv mongodb-linux-x86_64-ubuntu2004-4.4.4 ~/tools/mongodb
  ```
  
  把 mongodb 中的 `bin` 目录加入环境变量 `PATH`

  ```bash
  export PATH=/home/<username>/tools/mongodb/bin:$PATH
  ```

创建数据库目录, 可以自定义选择目录

```bash
mkdir -p /data/mongo/db
```

### 1.3 启动 MongoDB

MongoDB 的默认启动端口为 27017. 另外需要指定数据库的路径.

```bash
mongod --port 27017 --dbpath /data/mongo/db
```

### 1.4 在 Sacred 中使用 MongoDB

```python
from sacred import Experiment
from sacred.observers import MongoObserver

ex = Experiment('ExpName')
observer_mongo = MongoObserver.create(url='localhost:17000', db_name='ExpDBName')
ex.observers.append(observer_mongo)
```

### 1.5 使用配置文件

使用 MongoDB 配置文件可以简化启动流程, 配置文件的配置项与命令行选项是直接对应的. 
* 使用包管理工具安装的 MongoDB 会默认创建一个配置文件, Linux 下路径一般为 `/etc/mongod.conf`, Windows 下路径一般为 `<install directory>\bin\mongod.cfg`.
* 独立压缩包的 MongoDB 默认没有配置文件, 需要手动创建. 模板如下:

  ```
  processManagement:
      fork: true
  net:
      bindIp: localhost
      port: 27017
  storage:
      dbPath: /data/mongo/db
      journal:
          enabled: true
  systemLog:
     destination: file
     path: "/data/mongo/mongod.log"
     logAppend: true
  ```

  启动时使用 `--config` 或 `-f` 指定配置文件即可: `mongod --config /etc/mongod.conf`

### 1.6 MongoDB 的安全性

{% include card.html type="warning" title="MongoDB 安全性" content="MongoDB 默认不会开启任何安全措施, 存在被攻击的风险, 因此需要我们在建立数据库时就开启安全措施." %}

1. 启动不安全的 mongodb
  ```bash
  mongod --port 27017 --dbpath /data/mongo/db
  ```

2. 新开启一个终端, 连接到刚启动的 mongodb
  ```bash
  mongo --port 27017
  ```

3. 在 `admin` 数据库中新建管理员用户, 并设置密码. (下面的命令在 mongo 中执行)
  ```
  use admin
  db.createUser(
      {
          user: "myUserAdmin",
          pwd: passwordPrompt(), // 或者明文密码
          roles: [
              {
                  role: "userAdminAnyDatabase",
                  db: "admin"
              },
              {
                  role: "readWriteAnyDatabase",
                  db: "admin"
              }
          ]
      }
  )
  ```
  查看所有用户
  ```
  db.system.users.find().pretty()
  ```
  创建新的(非管理员)用户并赋予权限
  ```
  use myDB
  db.grantRolesToUser("jarvis", [{role: "readWrite", db: "myDB"}])
  ```
  删除某个权限
  ```
  use myDB
  db.revokeRolesFromUser("jarvis", [{role: "readWrite", db: "myDB"}])
  ```


4. 关闭刚刚的两个终端, 再重新启动 mongodb (同时开启访问控制)
  * 如果使用命令行启动, 则需要指定 `--auth` 参数, 否则会报错.
  ```bash
  mongod --auth --port 27017 --dbpath /data/mongo/db
  ```
  * 如果使用配置文件启动, 则需要在配置文件中添加:
  ```
  security:
      authorization: enabled
  ```
  
5. 现在连接到该数据库的客户端必须通过用户名和密码进行认证, 同时访问权限会受限制在指定的范围内.
  ```bash
  mongo --port 27017 --authenticationDatabase "admin" -u myUserAdmin -p
  # 或者
  mongo mongodb://myUserAdmin:xxxxxx@localhost:27017
  ```
  输入密码以登录数据库.


## 2. Omniboard 可视化

Omniboard 是一个用于机器学习实验管理库 Sacred 的基于网页的控制面板工具. 它可以使用 Sacred 中提供的工具连接到 MongoDB 数据库, 用来帮助可视化不同的实验和指标. Omniboard 使用 React, Node.js, Express 和 Bootstrap 编写.

{% include card.html type="info" content="从 v2.0 开始, Omniboard 只支持 MongoDB >=4.0" %}

### 2.1 使用 Docker 安装

拉取镜像

```bash
docker pull vivekratnavel/omniboard
```

开启容器, 把容器的 9000 端口映射到本地的 17001 端口, 连接到先前创建的网络 `sacred`, 指定数据库的配置 `sacred_mongo:27017:ExpName`, 其中 `ExpName` 为数据库名称, 需要与 Python 代码中的数据库对应.

```
docker run -p 17001:9000 --name omniboard --network sacred -d vivekratnavel/omniboard -m sacred_mongo:27017:ExpName
```

### 2.2 手动安装

安装 Node.js v8 或更高版本

1. 安装nvm (如果 install.sh 下载不下来的话, 就新建一个文件手动把代码复制过去, 再 bash install.sh 运行)
  ```bash
  curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash source　~/.bashrc
  ```

2. 安装Nodejs
  ```bash
  nvm install node
  ```

3. 安装 Omniboard
  ```bash
  npm install -g omniboard
  ```
  换源安装
  ```bash
  npm install -g omniboard --registry=https://registry.npm.taobao.org
  ```  
  永久换源安装
  ```bash
  npm config set registry https://registry.npm.taobao.org
  npm install -g omniboard
  ```

### 2.3 开启 Ominboard

```bash
omniboard -m localhost:27017:ExpDBName

PORT=17000 omniboard -m localhost:27017:ExpDBName
```

默认 omniboard 开启在 9000 端口. 如需要指定端口, 则使用 `PORT` 环境变量.


