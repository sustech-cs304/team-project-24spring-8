FROM node:14

WORKDIR /app

COPY package*.json ./

RUN npm config set registry https://registry.npmmirror.com

RUN npm install

COPY . .

RUN npm run build

EXPOSE 8080

CMD ["npm", "run", "serve"]
