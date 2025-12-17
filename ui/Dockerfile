# UI Dockerfile (React + Vite)
FROM node:18-alpine

WORKDIR /app

# Package dosyalarını kopyala
COPY package*.json ./

# Bağımlılıkları yükle
RUN npm install

# Uygulama kodunu kopyala
COPY . .

# Port expose et
EXPOSE 5173

# Development server başlat
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

