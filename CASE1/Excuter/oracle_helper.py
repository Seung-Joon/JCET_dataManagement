import cx_Oracle       

def connection(config):
    conn = cx_Oracle.connect(config["user_ID"],
                         config["user_PW"],
                         config["database_IP"] + ":" + config["database_Port"] + "/" + config["database_Sid"])

    return conn

def cursor(connection):
    return connection.cursor()

def execute(sql, cursor):
    cursor.execute(sql)

def get_datatable(sql, cursor):
    result = cursor.execute(sql)
    table_object = {}

    flag = 0
    for index in result:
        table_object[flag] = list(index)
        flag += 1

    return table_object

def commit(connection):
    connection.commit()


