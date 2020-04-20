from sql_source import *
from oracle_helper import *
from timeout import *
from models import *
import json

connectionString = {
    "user_ID": "rts",
    "user_PW": "rts4sck0",
    "database_IP": "10.20.20.56",
    "database_Port": "1521",
    "database_Sid": "SKCIMDWH",
} # DB 연결 정보


if __name__ == '__main__':
    db_connection = connection(connectionString)
    db_cursor = cursor(db_connection)
    
    res = get_datatable(error_lot(), db_cursor)
    print("Errror Data List\n")
    print(json.dumps(res, indent=4, sort_keys=True))

    
 
    for index in res.values():
        print("\ntarget-> ", index[0])
        print("excute procedure")

        execute(recover(index[0]), db_cursor) # 처리 프로시저 실행
        
        validation_res = get_datatable(result_check(index[0]), db_cursor) # 프로시저 결과 조회
        validation_res = validation_res[0]
        
        if validation_res[1] == "Y":
            print("success")
            execute(upt(validation_res[0]), db_cursor) # upt 업데이트

            print(get_datatable(result_check(validation_res[0]), db_cursor)) # 업데이트 결과 출력
            commit(db_connection)
        else:
            print("execute fail...")
    
    db_connection.close()
    print("\nEnd Of Report.")
        



