# Dockerfile
FROM node:20-slim

RUN apt-get update && apt-get install -y \
  wget \
  gnupg \
  ca-certificates \
  ffmpeg \
  libx11-xcb1 \
  libnss3 \
  libxcomposite1 \
  libxrandr2 \
  libxdamage1 \
  libasound2 \
  libatk1.0-0 \
  libatk-bridge2.0-0 \
  libpangocairo-1.0-0 \
  libxss1 \
  libgtk-3-0 \
  libx11-6 \
  libxext6 \
  libgbm1 \
  fonts-liberation \
  libdrm2 \
  libxshmfence1 \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
  
WORKDIR /app
COPY . .

RUN npm install
RUN npx playwright install --with-deps

CMD ["npx", "tsx", "src/index.ts"]
