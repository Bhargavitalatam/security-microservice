import base64
import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import urllib3

# This forces the connection to stay open and use IPv4
urllib3.util.connection.HAS_IPV6 = False

def run_test():
    try:
        # 1. Load the Public Key
        with open("data/keys/public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        # 2. Encrypt a test seed
        test_seed = b"MYSECRETSEED123"
        ciphertext = public_key.encrypt(
            test_seed,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encoded_seed = base64.b64encode(ciphertext).decode('utf-8')

        # 3. Send to the API using explicit 127.0.0.1
        response = requests.post(
            "http://127.0.0.1:8000/decrypt-seed",
            json={"encrypted_seed": encoded_seed},
            headers={"Connection": "close"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.json()}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == '__main__':
    run_test()
