import hashlib
import hmac
import random


class DH_KeyGenerator:
    def __init__(self, *args):
        if not args:
            self.public_g = random.randint(2 ** 10, 2 ** 40)
            self.public_p = random.randint(3**100, 3**300)
        else:
            self.public_g, self.public_p = args
        self.private_key = random.randint(10**50, 10**100)
        self.full_key = None

    def generate_partial_key(self):
        return (self.public_g ** self.private_key) % self.public_p

    def generate_full_key(self, partial_key):
        full_key = (partial_key ** self.private_key) % self.public_p
        self.full_key = full_key
        return full_key


def get_sign(private_key, session_challenge):
    return hmac.new(
        private_key.encode(),
        session_challenge.encode(),
        hashlib.sha256
    ).hexdigest()


def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
