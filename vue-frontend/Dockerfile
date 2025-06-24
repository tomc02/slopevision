# Build stage
FROM oven/bun:1.1-alpine AS build-stage

WORKDIR /app

# Copy necessary files for install/build
COPY package.json ./
COPY vite.config.js ./

# Install dependencies using Bun
RUN bun install

# Copy the rest of the source code
COPY . .
COPY .env.production ./
COPY .env.production ./.env

# Build the project using Bun
RUN bun run build

# Production stage
FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
