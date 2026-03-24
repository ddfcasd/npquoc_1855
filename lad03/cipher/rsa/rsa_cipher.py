import os
import rsa


class RSACipher:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.keys_dir = os.path.join(self.base_dir, "keys")
        self.public_key_path = os.path.join(self.keys_dir, "publicKey.pem")
        self.private_key_path = os.path.join(self.keys_dir, "privateKey.pem")

        if not os.path.exists(self.keys_dir):
            os.makedirs(self.keys_dir)

    def generate_keys(self):
        public_key, private_key = rsa.newkeys(512)

        with open(self.public_key_path, "wb") as pub_file:
            pub_file.write(public_key.save_pkcs1("PEM"))

        with open(self.private_key_path, "wb") as pri_file:
            pri_file.write(private_key.save_pkcs1("PEM"))

    def load_keys(self):
        with open(self.private_key_path, "rb") as pri_file:
            private_key = rsa.PrivateKey.load_pkcs1(pri_file.read())

        with open(self.public_key_path, "rb") as pub_file:
            public_key = rsa.PublicKey.load_pkcs1(pub_file.read())

        return private_key, public_key

    def encrypt(self, message, public_key):
        return rsa.encrypt(message.encode(), public_key)

    def decrypt(self, ciphertext, private_key):
        return rsa.decrypt(ciphertext, private_key).decode()

    def sign(self, message, private_key):
        return rsa.sign(message.encode(), private_key, "SHA-256")

    def verify(self, message, signature, public_key):
        try:
            rsa.verify(message.encode(), signature, public_key)
            return True
        except:
            return False