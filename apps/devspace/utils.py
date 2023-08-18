# utils.py
# utils.py
import secrets


def generate_keys():
    public_key = secrets.token_hex(
        16
    )  # Generate a random hex string of length 32 (16 bytes) for the public key
    secret_key = secrets.token_hex(
        20
    )  # Generate a random hex string of length 40 (20 bytes) for the secret key

    return public_key, secret_key
