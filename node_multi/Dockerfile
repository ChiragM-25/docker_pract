# Stage 1: Install dependencies
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install

# Stage 2: Runtime
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules node_modules
COPY . .
CMD ["node", "index.js"]