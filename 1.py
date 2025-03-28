import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

with open("test.txt", "rb") as f:  
    data = f.read()

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

start = time.time()
chunk_size = 190  
encrypted_data = b""
for i in range(0, len(data), chunk_size):
    chunk = data[i:i + chunk_size]
    encrypted_chunk = public_key.encrypt(
        chunk,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    encrypted_data += encrypted_chunk

decrypted_data = b""
chunk_size_enc = 256  
for i in range(0, len(encrypted_data), chunk_size_enc):
    chunk = encrypted_data[i:i + chunk_size_enc]
    decrypted_chunk = private_key.decrypt(
        chunk,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(), label=None)
    )
    decrypted_data += decrypted_chunk

end = time.time()
if data == decrypted_data:
    print(f"RSA 암호화/복호화 시간: {end - start} 초")

key = os.urandom(32)  
iv = os.urandom(16)   
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

start = time.time()
encryptor = cipher.encryptor()
padding_length = 16 - (len(data) % 16)  
padded_data = data + b"\0" * padding_length
encrypted_aes = encryptor.update(padded_data) + encryptor.finalize()

decryptor = cipher.decryptor()
decrypted_aes = decryptor.update(encrypted_aes) + decryptor.finalize()
decrypted_aes = decrypted_aes[:-padding_length] 
end = time.time()

if data == decrypted_aes:
    print(f"AES 암호화/복호화 시간: {end - start} 초")