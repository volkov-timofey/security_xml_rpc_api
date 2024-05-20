### Installation

Clone the repository and install manually:

##### Before installing, prepare your environment variables:
* DATABASE_URL
    > For example: DATABASE_URL=postgresql://user:password@localhost:5432/mydb
* SECRET_KEY
* URL_SERVER
* HOST
* PORT

```bash
$ git clone https://github.com/volkov-timofey/security_xml_rpc_api.git
$ cd security_xml_rpc_api
$ make init_run_server # build db and start server
$ make start_client
```