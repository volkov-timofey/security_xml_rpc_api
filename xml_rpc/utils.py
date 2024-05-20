import hashlib
import hmac
import random


class DH_KeyGenerator:
    """
    Implementation algorithm Diffie-Hellman
    A = g ** a mod p (partial_key client or server)
    B = g ** b mod p (partial_key client or server)

    private_key_1 = A ** b mod p -> g ** (b*a) mod p
    private_key_2 = B ** a mod p -> g ** (a*b) mod p

    """
    def __init__(self, *args):
        if not args:
            self.public_g = random.randint(100, 200)
            # random.randint(2 ** 10, 2 ** 40)
            self.public_p = random.randint(100, 200)
            # random.randint(3**100, 3**300)
        else:
            self.public_g, self.public_p = args
        self.private_key = random.randint(100, 200)
        # random.randint(10**50, 10**100)
        self.full_key = None

    def generate_partial_key(self):
        return (self.public_g ** self.private_key) % self.public_p

    def generate_full_key(self, partial_key):
        full_key = (partial_key ** self.private_key) % self.public_p
        self.full_key = full_key
        return full_key


def get_sign(private_key, session_challenge):
    """
    Generate sign with private_key and session_challenge
    """
    return hmac.new(
        private_key.encode(),
        session_challenge.encode(),
        hashlib.sha256
    ).hexdigest()


def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
