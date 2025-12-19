import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def run_crypto_ops():
    # 1. Load your Private Key to sign a commit hash
    with open("data/keys/private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)

    commit_hash = b"6a2ef45" # Your latest GitHub commit prefix
    
    # SIGNING: RSA-PSS with SHA-256 as per requirement
    signature = private_key.sign(
        commit_hash,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    
    with open("data/signature.bin", "wb") as f:
        f.write(signature)
    
    print(f"✅ Signed commit {commit_hash.decode()} using RSA-PSS.")
    print(f"✅ Signature saved to data/signature.bin")

if __name__ == "__main__":
    run_crypto_ops()