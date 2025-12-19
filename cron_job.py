import pyotp
import base64
import os
import datetime
from cryptography.hazmat.primitives import hashes

SEED_PATH = "data/seed.txt"
LOG_PATH = "cron_logs/totp_log.txt"

def run_job():
    if not os.path.exists(SEED_PATH):
        return
    
    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()
    
    b32_seed = base64.b32encode(seed.encode()).decode().replace('=', '')
    totp = pyotp.TOTP(b32_seed, interval=30, digits=6, digest=hashes.SHA1())
    code = totp.now()
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] TOTP Code: {code}\n"
    
    with open(LOG_PATH, "a") as log_file:
        log_file.write(log_entry)

if __name__ == "__main__":
    run_job()
