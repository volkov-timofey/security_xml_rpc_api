import datetime
import os
import secrets
from uuid import uuid4
from xmlrpc import server, client

from dotenv import load_dotenv

from xml_rpc.database import DataBase
from xml_rpc.utils import DH_KeyGenerator, get_sign, encrypt_password

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))


class XML_RPC_Server:
    """
    Class server part in XML RPC API
    """
    def __init__(self,
                 data_base: str = DATABASE_URL,
                 max_len_session_in_sec: int = 1800,
                 test_mode: bool = True):
        self.max_len_session_in_sec = max_len_session_in_sec
        self.data_base = data_base

        if test_mode:
            DataBase(self.data_base)._add_test_user()

    @staticmethod
    def is_not_active_session(data_session: tuple) -> bool:
        """
        Check session on activity
        """
        _, fin_session_time = data_session
        return fin_session_time < datetime.datetime.now()

    def authorization(self, login: str, password: str) -> client.dumps:
        """
        Method for authorization users
        """
        db = DataBase(self.data_base)
        hash_password = encrypt_password(password)
        current_user = db.get_pair_login_password(login)
        login_id, login, pass_from_db = current_user

        if not current_user or hash_password != pass_from_db:
            return client.dumps(
                client.Fault(401, 'Error authorization, please try again'),
                methodresponse=True
            )

        start_session_time = datetime.datetime.now()
        fin_session_time = start_session_time + datetime.timedelta(
            seconds=self.max_len_session_in_sec)
        # многие переходят на NanoID,
        # но этого инструмента нет в стандартном наборе
        # uuid4 - рандомное представление
        # без задействования чувствительных данных
        session_id = str(uuid4())

        db.add_session(
            session_id,
            login_id,
            start_session_time,
            fin_session_time
        )

        return client.dumps((session_id,), methodresponse=True)

    def get_secret(self, session_id: str, partial_client_key: str,
                   public_g: str, public_p: str):
        """
        Generate private key with algorithm Diffie-Hellman
        with client public data
        """
        db = DataBase(self.data_base)

        if self.is_not_active_session(db.get_active_session(session_id)):
            return client.dumps(
                client.Fault(
                    401,
                    "Your session is terminate, please start new session"
                ),
                methodresponse=True
            )
        gen_server_key = DH_KeyGenerator(public_g, public_p)
        partial_server_key = gen_server_key.generate_partial_key()
        private_key = gen_server_key.generate_full_key(partial_client_key)

        db.add_private_key(session_id, private_key)

        return client.dumps((partial_server_key,), methodresponse=True)

    def get_challenge(self, session_id: str) -> client.dumps:
        """
        Get random challenge
        """
        db = DataBase(self.data_base)

        if self.is_not_active_session(db.get_active_session(session_id)):
            return client.dumps(
                client.Fault(
                    401,
                    'Your session is terminate, please start new session'
                ),
                methodresponse=True
            )

        session_challenge = secrets.token_urlsafe()
        db.add_challenge(session_id, session_challenge)

        return client.dumps((session_challenge,), methodresponse=True)

    def read_data_from_db(
            self, session_id: str, client_sign: str
    ) -> client.dumps:
        """
        Get sample data for future response

        in this example - terminate session
        """
        db = DataBase(self.data_base)
        if self.is_not_active_session(db.get_active_session(session_id)):
            return client.dumps(
                client.Fault(
                    401,
                    'Your session is terminate, please start new session'
                )
            )
        private_key, session_challenge = db.get_session_data(session_id)
        server_sign = get_sign(private_key, session_challenge)

        if server_sign != client_sign:
            return client.dumps(
                client.Fault(
                    403,
                    'Access Denied – You don’t have permission to access, \
                     please try authorization again.'
                )
            )

        return client.dumps((db.get_last_session_id(),), methodresponse=True)


if __name__ == '__main__':
    server = server.SimpleXMLRPCServer((HOST, PORT))
    server.register_instance(XML_RPC_Server())
    print('Server run, can to start client')
    server.serve_forever()
