FROM node:18-alpine

WORKDIR /app

# Create a non-root user for security
RUN addgroup appuser && \
    adduser -D -G appuser appuser && \
    chown -R appuser:appuser /app

# Copy package files first for better layer caching
COPY package*.json .
RUN npm ci --omit=dev

# Copy application code
COPY app.js .

USER appuser

EXPOSE 5000

CMD ["npm", "start"]
