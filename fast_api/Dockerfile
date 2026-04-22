FROM python:3.11-slim

WORKDIR /app

# Create a non-root user for security and set permissions
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
