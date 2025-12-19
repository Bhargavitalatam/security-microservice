import hashlib
import pyotp
import base64
import os
import datetime

# REQUIREMENT: Paths must match the evaluator's expected volume structure
SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"

def run_job():
    # Ensure the directory exists to prevent write errors
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    if not os.path.exists(SEED_PATH):
        return
    
    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()
    
    # REQUIREMENT: Use SHA-1 algorithm and 6-digit codes
    # base64.b32encode is used to create a valid secret for pyotp
    secret = base64.b32encode(seed.encode()).decode().replace('=', '')
    totp = pyotp.TOTP(secret, digest=hashlib.sha1)
    code = totp.now()
    
    # REQUIREMENT: Format must be YYYY-MM-DD HH:MM:SS
    # Instructions require UTC timestamps
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    
    # REQUIREMENT: Log format specified as "YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX"
    log_entry = f"{timestamp} - 2FA Code: {code}\n"
    
    with open(LOG_PATH, "a") as log_file:
        log_file.write(log_entry)

if __name__ == "__main__":
    run_job()