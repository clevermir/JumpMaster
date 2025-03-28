from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

class ECDSA:
    def __init__(self, p, q, e1):
        self.p = p
        self.q = q
        self.e1 = e1 

    def sign(self, M, d):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(M.encode())
        h = int.from_bytes(digest.finalize(), "big") % self.q

        while True:
            r = int.from_bytes(os.urandom(32), "big") % (self.q - 1) + 1
            P = ec.derive_private_key(r, ec.SECP256K1()).public_key().public_numbers()
            S1 = P.x % self.q
            if S1 == 0:
                continue
            r_inv = pow(r, -1, self.q)  
            S2 = (h + d * S1) * r_inv % self.q
            if S2 != 0:
                break
        return S1, S2

    def verify(self, M, S1, S2, e2):
        digest = hashes.Hash(hashes.SHA256())
        digest.update(M.encode())
        h = int.from_bytes(digest.finalize(), "big") % self.q

        S2_inv = pow(S2, -1, self.q)  
        A = (h * S2_inv) % self.q
        B = (S1 * S2_inv) % self.q
        print(f"A = {hex(A)}")
        print(f"B = {hex(B)}")

        curve = ec.SECP256K1()
        e1_point = ec.EllipticCurvePublicNumbers(self.e1[0], self.e1[1], curve).public_key()
        e2_point = ec.EllipticCurvePublicNumbers(e2[0], e2[1], curve).public_key()
        T = (A * e1_point + B * e2_point).public_numbers()
        return (T.x % self.q) == S1

from ecdsa import *
private_key = ec.generate_private_key(ec.SECP256K1())
d = private_key.private_numbers().private_value
public_key = private_key.public_key()
e2 = (public_key.public_numbers().x, public_key.public_numbers().y)

print(f"개인 키 = {hex(d)}")
print(f"공개 키 = ({hex(e2[0])}, {hex(e2[1])})")

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

algorithm = ECDSA(p, q, G)
M = input("메시지? ")
S1, S2 = algorithm.sign(M, d)
print(f"1. Sign:\n\tS1 = {hex(S1)}\n\tS2 = {hex(S2)}")

print("2. 정확한 서명을 입력할 경우:")
if algorithm.verify(M, S1, S2, e2):
    print("검증 성공")
else:
    print("검증 실패")

print("3. 잘못된 서명을 입력할 경우:")
if algorithm.verify(M, S1-1, S2-1, e2):
    print("검증 성공")
else:
    print("검증 실패")