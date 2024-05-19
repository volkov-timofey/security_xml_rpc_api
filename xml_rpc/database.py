import psycopg2
import datetime

from xml_rpc.utils import encrypt_password


class DataBase:
    """
    Class for connecting to a user database
    """
    def __init__(self, database_url: str):
        """
        Environment variable
        For example: postgresql://user:password@localhost:5432/mydb
        """
        self.database_url = database_url

    def _connect_db(self) -> psycopg2.connect:
        """
        Connection in database
        """
        try:
            return psycopg2.connect(self.database_url)

        except ValueError:
            print('Can`t establish connection to database')

    @staticmethod
    def _close_connect_db(connect) -> None:
        """
        Closing connect to database
        """
        connect.close()

    def get_pair_login_password(self, login: str, password: str) -> list:
        """
        Check information about user
        """
        connect = self._connect_db()
        requests_ = """
            SELECT *
            FROM accounts
            WHERE login = %s and password = %s;"""
        with connect.cursor() as cursor:
            cursor.execute(requests_, (login, password,))
            result = cursor.fetchall()
        self._close_connect_db(connect)
        return result

    def add_session(
            self,
            session_id: str,
            login: str,
            start_session_time: datetime,
            fin_session_time: datetime
    ):
        """
        Add information users session
        """
        request_ = """
            INSERT INTO sessions \
            (session_id, login, start_session_time, fin_session_time) \
            VALUES (%s, %s, %s, %s,);
            """

        connect = self._connect_db()
        with connect.cursor() as cursor:
            cursor.execute(
                request_,
                (session_id, login, start_session_time, fin_session_time)
            )
        connect.commit()
        self._close_connect_db(connect)

    def is_active_session(self, session_id: str) -> bool:
        """
        Get status session -> bool
        """
        connect = self._connect_db()
        request_ = """
                    SELECT fin_session_time
                    FROM sessions
                    WHERE session_id = %s;"""
        with connect.cursor() as cursor:
            cursor.execute(request_, (session_id,))
            result = cursor.fetchall()
        self._close_connect_db(connect)

        return datetime.datetime.now() < result[0]

    def add_private_key(self, session_id: str, private_key: str) -> None:
        """
        Save private key user in sessions_data
        """
        request_ = """
                    INSERT INTO sessions_data \
                    (session_id, private_key) \
                    VALUES (%s, %s,);
                    """

        connect = self._connect_db()
        with connect.cursor() as cursor:
            cursor.execute(
                request_,
                (session_id, private_key)
            )
        connect.commit()
        self._close_connect_db(connect)

    def add_challenge(self, session_id: str, active_challenge: str) -> None:
        """
        Save challenge user in sessions_data
        """
        request_ = """
            INSERT INTO sessions_data \
            (session_id, active_challenge) \
            VALUES (%s, %s,);
            """

        connect = self._connect_db()
        with connect.cursor() as cursor:
            cursor.execute(
                request_,
                (session_id, active_challenge)
            )
        connect.commit()
        self._close_connect_db(connect)

    def get_session_data(self, session_id: str) -> list:
        """
        Get private key and challenge user in sessions_data
        """
        connect = self._connect_db()
        requests_ = """
            SELECT private_key, current_challenge
            FROM sessions_data
            WHERE session_id = %s;"""
        with connect.cursor() as cursor:
            cursor.execute(requests_, (session_id,))
            result = cursor.fetchall()
        self._close_connect_db(connect)
        return result

    def _add_test_user(
            self, login: str = 'login', password: str = 'password'
    ) -> None:
        """
        Get private key and challenge user in sessions_data
        """
        connect = self._connect_db()
        requests_ = """
            INSERT INTO accounts \
            (login, password) \
            VALUES (%s, %s,);
            """
        with connect.cursor() as cursor:
            cursor.execute(requests_, (login, encrypt_password(password)))
        connect.commit()
        self._close_connect_db(connect)
