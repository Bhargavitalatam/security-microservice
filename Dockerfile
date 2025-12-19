# Stage 1: Builder
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app

# Set timezone to UTC
ENV TZ=UTC
RUN apt-get update && apt-get install -y cron tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# REQUIREMENT: Create exact volume mount points required by evaluator
RUN mkdir -p /data /cron

# REQUIREMENT: Cron must log to /cron/last_code.txt
RUN echo "* * * * * /usr/local/bin/python /app/cron_job.py >> /cron/last_code.txt 2>&1" > /etc/cron.d/totp-cron
RUN chmod 0644 /etc/cron.d/totp-cron
RUN crontab /etc/cron.d/totp-cron

# REQUIREMENT: Expose port 8080
EXPOSE 8080

# Start script running FastAPI on 8080 using uvicorn
RUN echo "#!/bin/sh\ncron\nuvicorn main:app --host 0.0.0.0 --port 8080" > start.sh
RUN chmod +x start.sh

CMD ["./start.sh"]