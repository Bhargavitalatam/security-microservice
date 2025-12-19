\# Security \& 2FA Microservice



A containerized Python microservice demonstrating industrial-grade security implementations, including asymmetric RSA encryption and RFC-6238 compliant TOTP generation.



\## 🚀 Key Features

\- \*\*RSA-4096 Encryption\*\*: Securely receive and decrypt seeds using asymmetric public/private key pairs.

\- \*\*TOTP Generation\*\*: Real-time generation of 2FA codes compatible with Google Authenticator.

\- \*\*Dockerized Cron\*\*: An internal background daemon that logs security codes every 60 seconds.

\- \*\*Multi-Stage Build\*\*: Optimized Docker image for high performance and low security footprint.



\## 🛠 Tech Stack

\- \*\*Language\*\*: Python 3.11

\- \*\*Framework\*\*: FastAPI

\- \*\*Security\*\*: Cryptography (RSA/Padding), PyOTP

\- \*\*Deployment\*\*: Docker \& Docker Compose



\## 📦 Architecture

The service runs in a secure Docker container with persistent volumes for sensitive data:

\- `/app/data`: Stores RSA keys and the decrypted seed.

\- `/app/cron\_logs`: Stores automated security heartbeats.



\## 🏁 Quick Start

1\. \*\*Launch with Docker:\*\*

&nbsp;  ```bash

&nbsp;  docker-compose up --build -d

