from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os
import pyotp
import time

app = FastAPI()

SEED_STORAGE_PATH = "data/seed.txt"
PRIVATE_KEY_PATH = "data/keys/private_key.pem"

class SeedRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

@app.post("/decrypt-seed")
async def decrypt_seed(request: SeedRequest):
    try:
        with open(PRIVATE_KEY_PATH, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)
        ciphertext = base64.b64decode(request.encrypted_seed)
        decrypted_seed = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        with open(SEED_STORAGE_PATH, "wb") as f:
            f.write(decrypted_seed)
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa():
    if not os.path.exists(SEED_STORAGE_PATH):
        raise HTTPException(status_code=500, detail="Seed unavailable")
    with open(SEED_STORAGE_PATH, "r") as f:
        raw_seed = f.read().strip()
    b32_seed = base64.b32encode(raw_seed.encode()).decode().replace('=', '')
    totp = pyotp.TOTP(b32_seed, interval=30, digits=6, digest=hashes.SHA1())
    return {"code": totp.now(), "valid_for": 30 - (int(time.time()) % 30)}

@app.post("/verify-2fa")
async def verify_2fa(request: VerifyRequest):
    if not os.path.exists(SEED_STORAGE_PATH):
        raise HTTPException(status_code=400, detail="Seed missing")
    with open(SEED_STORAGE_PATH, "r") as f:
        raw_seed = f.read().strip()
    b32_seed = base64.b32encode(raw_seed.encode()).decode().replace('=', '')
    totp = pyotp.TOTP(b32_seed, interval=30, digits=6, digest=hashes.SHA1())
    
    # valid_window=1 provides the ±1 period tolerance (30s before/after)
    if totp.verify(request.code, valid_window=1):
        return {"status": "valid"}
    else:
        return {"status": "invalid"}

import hashlib
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
class VerifyRequest(BaseModel):
    code: str

@app.post("/verify-2fa")
async def verify_2fa(payload: VerifyRequest):
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed unavailable")
    
    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()
    
    totp = pyotp.TOTP(base64.b32encode(seed.encode()).decode())
    # valid_window=1 allows for +/- 30 seconds as per requirements
    is_valid = totp.verify(payload.code, valid_window=1)
    
    if is_valid:
        return {"status": "verified"}
    else:
        raise HTTPException(status_code=400, detail="Invalid code")
