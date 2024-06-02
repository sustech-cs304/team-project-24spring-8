# 开发文档

## 系统概览

本文档详细描述了基于FastAPI框架、SQLAlchemy ORM以及SQLite数据库构建的后端API服务。该系统支持用户、事件、帖子、评论以及通知的管理，并提供了一个具有完整功能的Web接口，适用于需要用户互动和事件管理功能的应用。

## 技术栈

- **FastAPI**: 高性能的Web框架，用于快速构建API，支持异步请求处理。
- **SQLAlchemy**: Python的SQL工具包和对象关系映射器，提供了全面的系统用于数据库操作。
- **SQLite**: 轻量级的关系数据库，存储在本地的文件中，适合小型项目和原型开发。
- **Pydantic**: 用于数据解析和验证的库，通过Python类型注解提供自动数据验证功能。
- **python-jose**: 一个JavaScript Object Signing and Encryption的Python实现，用于处理JWT令牌。

## 环境配置

### 安装依赖

在项目开始前，请确保安装以下必要的库：

- Python 3.7 及以上
- FastAPI
- Uvicorn（用于运行FastAPI应用）
- SQLAlchemy
- python-jose（用于处理JWT）

您可以使用如下命令来安装上述依赖：

```bash
pip install fastapi uvicorn sqlalchemy pydantic "python-jose[cryptography]"
```

### 数据库初始化

在项目的根目录下创建一个名为 `init_db.py` 的Python脚本，以设置和初始化数据库。此脚本应包含以下功能：

1. 创建数据库表。
2. 加载测试数据。

### 项目结构

建议的项目目录结构如下：

```plaintext
/your-project
|-- /app
|   |-- __init__.py
|   |-- main.py
|   |-- models.py
|   |-- schemas.py
|   |-- dependencies.py
|   |-- routers
|       |-- __init__.py
|       |-- users.py
|       |-- events.py
|       |-- posts.py
|-- /tests
|   |-- __init__.py
|   |-- test_main.py
|   |-- test_models.py
|-- requirements.txt
|-- README.md
|-- .env (for environment variables)
```

## 数据库模型

### 用户模型 `User`

| 字段              | 类型    | 描述               |
|------------------|-------|-------------------|
| id               | int   | 主键，唯一标识用户  |
| username         | str   | 用户名，必须唯一     |
| email            | str   | 用户邮箱，必须唯一   |
| full_name        | str   | 用户全名            |
| hashed_password  | str   | 加密后的密码         |

### 事件模型 `Event`

| 字段              | 类型          | 描述                 |
|------------------|-------------|---------------------|
| id               | int         | 主键，唯一标识事件    |
| name             | str         | 事件名称             |
| event_time       | datetime    | 事件具体时间           |
| description      | str         | 事件描述             |
| duration_hours   | int         | 持续时间（小时）       |
| duration_minutes | int         | 持续时间（分钟）       |
| tickets_sold     | int         | 已售出的票数           |
| max_tickets      | int         | 可售出的最大票数        |

### 帖子模型 `Post`

| 字段         | 类型     | 描述             |
|------------|--------|----------------|
| id          | int    | 主键，唯一标识帖子 |
| title       | str    | 帖子标题          |
| content     | str    | 帖子内容          |
| owner_id    | int    | 帖子作者的用户ID   |

### 评论模型 `Comment`

| 字段       | 类型  | 描述        |
| -------- | --- | --------- |
| id       | int | 主键，唯一标识评论 |
| content  | str | 评论内容      |
| event_id | int | 关联的事件ID   |
| owner_id | int | 发表评论的用户ID |

### 通知模型 `Notification`

| 字段         | 类型     | 描述             |
|------------|--------|----------------|
| id          | int    | 主键，唯一标识通知 |
| message     | str    | 通知内容          |
| created_at  | datetime | 创建时间          |
| sender      | str    | 发送者姓名         |
| owner_id    | int    | 接收者的用户ID     |

## API端点

[详细描述每个API端点的用途、请求方法、路径、参数、请求体、响应体及状态码。]

### 用户管理

#### 创建用户

- **Endpoint**: `POST /users/`
- **功能**: 注册新用户
- **请求体**:
  - `username`: str - 必填，新用户的用户名
  - `email`: str - 必填，用户的电子邮箱
  - `full_name`: str - 可选，用户的全名
  - `hashed_password`: str - 必填，用户的密码（加密后）

- **响应**:
  - `200 OK`: 用户创建成功
  - `400 Bad Request`: 请求数据格式错误或缺少必要信息

#### 获取用户信息

- **Endpoint**: `GET /users/{user_id}`
- **功能**: 根据用户ID获取用户详细信息
- **参数**:
  - `user_id`: int - URL路径参数，用户的唯一标识符

- **响应**:
  - `200 OK`: 请求成功，返回用户信息
  - `404 Not Found`: 指定ID的用户不存在

#### 更新用户信息

- **Endpoint**: `PUT /users/{user_id}`
- **功能**: 更新用户详细信息
- **参数**:
  - `user_id`: int - URL路径参数，用户的唯一标识符

- **请求体**:
  - `username`: str - 必填，用户的新用户名
  - `email`: str - 必填，用户的新电子邮箱
  - `full_name`: str - 可选，用户的全名
  - `hashed_password`: str - 必填，用户的新密码（加密后）

- **响应**:
  - `200 OK`: 用户信息更新成功
  - `400 Bad Request`: 请求数据格式错误或缺少必要信息
  - `404 Not Found`: 指定ID的用户不存在

### 事件管理

#### 创建事件

- **Endpoint**: `POST /events/`
- **功能**: 创建一个新的事件
- **请求体**:
  - `name`: str - 必填，事件的名称
  - `event_time`: datetime - 必填，事件具体举行的时间
  - `description`: str - 必填，事件的描述
  - `duration_hours`: int - 必填，事件持续的小时数
  - `duration_minutes`: int - 必填，事件持续的分钟数
  - `tickets_sold`: int - 可选，默认为0，已售出的票数
  - `max_tickets`: int - 必填，最大可售票数

- **响应**:
  - `200 OK`: 事件创建成功
  - `400 Bad Request`: 请求数据格式错误或缺少必要信息

#### 查询事件

- **Endpoint**: `GET /events/`
- **功能**: 获取事件列表，支持分页和搜索
- **参数**:
  - `skip`: int - 可选，跳过的记录数，默认为0
  - `limit`: int - 可选，返回的记录数，默认为10
  - `search`: str - 可选，搜索关键词

- **响应**:
  - `200 OK`: 请求成功，返回事件列表
  - `204 No Content`: 没有事件满足条件

### 帖子管理

#### 发布帖子

- **Endpoint**: `POST /posts/`
- **功能**: 发布一个新帖子
- **请求体**:
  - `title`: str - 必填，帖子的标题
  - `content`: str - 必填，帖子的内容

- **响应**:
  - `200 OK`: 帖子发布成功
  - `400 Bad Request`: 请求数据格式错误或缺少必要信息

#### 查询帖子

- **Endpoint**: `GET /posts/`
- **功能**: 获取帖子列表
- **响应**:
  - `200 OK`: 请求成功，返回帖子列表
  - `204 No Content`: 没有帖子

### 评论管理

#### 发布评论

- **Endpoint**: `POST /comments/{event_id}`
- **功能**: 对某个事件发布评论
- **参数**:
  - `event_id`: int - URL路径参数，事件的唯一标识符

- **请求体**:
  - `content`: str - 必填，评论的内容

- **响应**:
  - `200 OK`: 评论发布成功
  - `400 Bad Request`: 请求数据格式错误或缺少必要信息
  - `404 Not Found`: 指定ID的事件不存在

#### 查询评论

- **Endpoint**: `GET /comments/{event_id}`
- **功能**: 获取某个事件的所有评论
- **参数**:
  - `event_id`: int - URL路径参数，事件的唯一标识符

- **响应**:
  - `200 OK`: 请求成功，返回评论列表
  - `204 No Content`: 该事件没有评论

### 通知管理

#### 发送通知

- **Endpoint**: `POST /notifications/`
- **功能**: 发送一个新通知
- **请求体**:
  - `message`: str - 必填，通知的消息内容
  - `sender`: str - 必填，发送者姓名

- **响应**:
  - `200 OK`: 通知发送成功
  - `400 Bad Request`: 请求数据格式错误或缺少必要信息

#### 查询通知

- **Endpoint**: `GET /notifications/`
- **功能**: 获取用户的所有通知
- **响应**:
  - `200 OK`: 请求成功，返回通知列表
  - `204 No Content`: 用户没有通知

## 安全性

本系统使用JWT进行用户身份验证和授权。每个需要验证的API端点都将检查请求中的JWT，确保只有授权的用户才能访问敏感数据。

### 实施JWT

- 使用 `python-jose` 库生成和验证JWT。
- 设置密钥和算法（例如：HS256）。
- 为每个登录用户生成一个JWT，包含用户的ID和有效时间。

## 启动应用

要启动应用，请运行以下命令：

```bash
uvicorn app.main:app --port 8001 --reload
```

这将在8001端口上启动应用，并允许代码更改后自动重新加载。

## 开发建议

- **数据一致性**: 使用SQLAlchemy的事务管理功能来保证数据的一致性。
- **数据库备份**: 定期备份数据库文件，防止数据丢失。
- **使用HTTPS**: 在部署到生产环境时，应确保应用通过HTTPS运行，增强数据传输的安全性。
- **错误处理**: 实现全局错误处理，确保所有API错误都以一致的格式返回。
- **性能优化**: 利用FastAPI的异步特性来处理I/O密集型任务，提高应用的响应速度和吞吐量。