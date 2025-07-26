# Dockerfile
FROM node:20-slim

WORKDIR /app
COPY . .

RUN npm install
RUN npx playwright install --with-deps

CMD ["npx", "tsx", "src/index.ts"]
