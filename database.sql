--noqa: disable=L010
DROP TABLE IF EXISTS accounts, accounts_data, sessions, sessions_data;
CREATE TABLE accounts (
	id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
	login varchar(255) NOT NULL,
	password varchar(255) NOT NULL
);

CREATE TABLE sessions (
    session_id varchar(255) PRIMARY KEY,
    login varchar(255) references accounts(login) NOT NULL,
    start_session_time timestamp,
    fin_session_time timestamp
);

CREATE TABLE sessions_data (
    session_id varchar(255) PRIMARY KEY references sessions(session_id),
    private_key varchar(255) NOT NULL,
    current_challenge varchar(255)
);