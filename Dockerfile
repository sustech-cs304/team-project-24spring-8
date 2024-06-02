# 第一阶段：构建 Vue.js 应用程序
FROM node:14 AS build-vue
WORKDIR /app
# 复制前端代码到容器中
COPY ./frontend/package*.json ./
# 使用 npm 镜像
RUN npm config set registry https://registry.npmmirror.com
# 安装依赖
RUN npm install
COPY ./frontend/ .
# 构建项目
RUN npm run serve

# 第二阶段：设置 FastAPI 应用
FROM python:3.9-slim
WORKDIR /code

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装 Python 依赖
COPY ./backend/requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 复制 FastAPI 应用代码到容器中
COPY ./backend /code/app

# 从第一阶段复制 Vue.js 构建的静态文件到 FastAPI 静态文件目录
COPY --from=build-vue /app/dist /code/app/static

# 启动 FastAPI 应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
