# 使用官方的 Node.js 镜像作为基础镜像
FROM node:14

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 package-lock.json 并安装 Node.js 依赖
COPY package*.json ./

RUN npm config set registry https://registry.npmmirror.com

RUN npm install

# 复制项目文件到工作目录
COPY . .

# 构建前端应用
RUN npm run build

# 暴露应用端口
EXPOSE 8080

# 启动前端应用
CMD ["npm", "run", "serve"]
