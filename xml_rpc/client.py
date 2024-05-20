import os
from xmlrpc import client

from dotenv import load_dotenv

from xml_rpc.utils import DH_KeyGenerator, get_sign

load_dotenv()

URL_SERVER = os.getenv('URL_SERVER')


class XML_RPC_Client:
    """
    Class client part in XML RPC API
    """
    def __init__(self, server_proxy: str):
        self.proxy = client.ServerProxy(server_proxy)
        self.session_id = None
        self.private_key = None
        self.challenge = None

    def authorization(self, login: str, password: str) -> str:
        """
        Method for authorization users
        """
        response = self.proxy.authorization(login, password)
        try:
            response = client.loads(response)
            self.session_id = response[0][0]
            return self.session_id
        except client.Fault as f:
            print(f.faultString)

    def generate_private_key(self) -> str:
        """
        Generate private key with algorithm Diffie-Hellman
        """
        generator_client_key = DH_KeyGenerator()
        partial_client_key = generator_client_key.generate_partial_key()

        response = self.proxy.get_secret(
            self.session_id,
            partial_client_key,
            generator_client_key.public_g,
            generator_client_key.public_p
        )
        try:
            partial_server_key = client.loads(response)[0][0]
            self.private_key = generator_client_key.generate_full_key(
                partial_server_key
            )

            return self.private_key

        except client.Fault as f:
            print(f.faultString)

    def get_challenge(self) -> str:
        """
        Get random challenge
        """
        response = self.proxy.get_challenge(self.session_id)

        try:
            self.challenge = client.loads(response)[0][0]
            return self.challenge
        except client.Fault as f:
            print(f.faultString)

    def read_data_from_db(self) -> str:
        """
        Read need information with check sign
        """
        sign = get_sign(self.private_key, self.challenge)

        response = self.proxy.read_data_from_db(self.session_id, sign)
        try:
            value = client.loads(response)[0][0]
            return value
        except client.Fault as f:
            print(f.faultString)


if __name__ == '__main__':
    client_ = XML_RPC_Client(URL_SERVER)
    print(client_.authorization('login', 'password'))
    print(client_.generate_private_key())
    print(client_.get_challenge())
