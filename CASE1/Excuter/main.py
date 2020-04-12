from sql_source import *
from oracle_helper import *

connectionString = {
    "user_ID": "rts",
    "user_PW": "rts4sck0",
    "database_IP": "10.20.20.56",
    "database_Port": "1521",
    "database_Sid": "SKCIMDWH",
} # DB 연결 정보


if __name__ == '__main__':
    res = datatable(Read.error_lot(), connection(connectionString))


    print(res)