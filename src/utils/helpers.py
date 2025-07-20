import hashlib
from src.utils.Constants import ADMIN_TOKEN


def get_admin_hash():

    # Encode the string to bytes
    encoded_string = ADMIN_TOKEN.encode("utf-8")

    # Create a SHA256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the encoded string
    sha256_hash.update(encoded_string)

    # Get the hexadecimal representation of the hash
    return sha256_hash.hexdigest()


if __name__ == "__main__":
    print(get_admin_hash())
