# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Install cron and clean up
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Setup Cron
# Create the cron tab: run every minute, use absolute paths
RUN echo "* * * * * /usr/local/bin/python /app/cron_job.py >> /var/log/cron.log 2>&1" > /etc/cron.d/totp-cron
RUN chmod 0644 /etc/cron.d/totp-cron
RUN crontab /etc/cron.d/totp-cron

# Expose API port
EXPOSE 8000

# Start script to run both Cron and FastAPI
RUN echo "#!/bin/sh\ncron\npython main.py" > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]
