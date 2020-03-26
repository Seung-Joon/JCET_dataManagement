# -*- coding:utf-8 -*-
import Case1_Sql_Source as sql
import os
import cx_Oracle
import pandas as pd
import sys

connectionString = {
    "user_ID": "rts",
    "user_PW": "rts4sck0",
    "database_IP": "10.20.20.56",
    "database_Port": "1521",
    "database_Sid": "SKCIMDWH",
} # DB 연결 정보

connection = sql.Init.Connection(connectionString) #DB 연결

class NoDataException(Exception):
    pass

if __name__ == "__main__":
    #print("Case1 에러 데이터 받아오는중...\n")
    dataSets = sql.SqlGet.Data_Case1Err_LotID(connection)
    if (len(list(dataSets)) == 0): raise NoDataException() #에러 처리된 데이터가 없을경우 에러 발생하여 레포트 생성 안되도록 함.

    print("< Data Error Report. Generated Date: " + sys.argv[1] + ' ' + sys.argv[2] + " >\n")
    print("Error Data List ↓\n")

    columns_id = [' [LOTID]', ' [Error Message]']
    data = list(map(list, dataSets)) # COM_LOCATION 별 데이터를 리스트 형태로 저장함
    print(pd.DataFrame(data, columns=columns_id)) # 데이터 차트 표시

    print('\n')

    for index in data:
        print("<" + index[0] + ">")
        print("===============================================================================")
        # COMPART가 NULL로 처리된 에러 데이터 가져옴
        cursor = connection.cursor()
        cursor.execute(sql.FormatSQL.Query_getDataComLocationNull(index[0]))

        columns_id = ['     [EQUIP_ID]', '     [STRIP_ID]', '     [COM_LOCATION]', '     [CREATED_TIME]']
        errData = list(map(list, cursor))
        print(pd.DataFrame(errData, columns=columns_id)) # 데이터 차트 표시
        print("\netc...")
        print("===============================================================================\n")

