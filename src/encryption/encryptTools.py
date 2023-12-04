from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA1, HMAC
from Crypto import Random

# Function that takes the password and path to encrypted file and returns decrypted string
def decrypt(password, file_path):
    with open(file_path, 'rb') as file:
        # Read the entire file content
        encrypted_data = file.read()

    # Extract IV (Initialization Vector) from the first 16 bytes of data
    IV = encrypted_data[:16]

    # Extract the actual data to decrypt (excluding the IV)
    data_to_decrypt = encrypted_data[16:]

    # Derive the key using PBKDF2 with SHA1 hash algorithm
    key = PBKDF2(password, IV, dkLen=16, count=100, prf=lambda p, s: HMAC.new(p, s, SHA1).digest())

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, IV)

    # Decrypt the data and unpad it with PKCS7
    decrypted_data = unpad(cipher.decrypt(data_to_decrypt), AES.block_size, style='pkcs7')

    # Convert the result to a string (assuming the original data was a string)
    decrypted_string = decrypted_data.decode('utf-8')

    return decrypted_string

# Function that takes the password and path to decrypted file and returns encrypted data
def encrypt(password, file_path):
    # Read the content from the file
    with open(file_path, 'rb') as decrypted_file:
        data_to_encrypt = decrypted_file.read()

    # Generate a random IV (Initialization Vector)
    IV = Random.new().read(16)

    # Derive the key using PBKDF2 with SHA1 hash algorithm
    key = PBKDF2(password, IV, dkLen=16, count=100, prf=lambda p, s: HMAC.new(p, s, SHA1).digest())

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, IV)

    # Pad the data with PKCS7 before encryption
    padded_data = pad(data_to_encrypt, AES.block_size, style='pkcs7')

    # Encrypt the data
    encrypted_data = IV + cipher.encrypt(padded_data)

    return encrypted_data
