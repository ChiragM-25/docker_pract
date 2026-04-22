FROM node:18-alpine

WORKDIR /app

# Create a non-root user for security & Change ownership to non-root user
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /app

# Copy package files first for better layer caching
COPY package*.json .
RUN npm ci --only=production

# Copy application code
COPY app.js .

USER appuser

EXPOSE 5000

CMD ["npm", "start"]
