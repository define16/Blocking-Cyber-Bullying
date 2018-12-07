from django.db import connection


def insert_dataSet(tableName, data):
    sql = "INSERT INTO " + tableName + " (coments) SELECT '" + str(
        data) + "' FROM DUAL WHERE NOT EXISTS (SELECT coments FROM " + tableName + " WHERE coments='" + str(data) + "')"
    print("DataSet : " + sql)
    connection.cursor().execute(sql)

    connection.commit()

def register_coments(id,coments, isbullying):
    sql = "INSERT INTO comentscotent (id, coments, isbullying) VALUES('"+ str(id) + "', '" + str(coments) + "', '" + int(isbullying)  + "')"

    print(sql)
    connection.cursor().execute(sql)

    connection.commit()

def select_dataSet(tableName) :
    cursor = connection.cursor();
    sql = "select coments from " + tableName
    cursor.execute(sql)
    context = []
    # 데이타 Fetch
    rows = cursor.fetchall()
    for row in rows :
        context.append(str(row))
    # print(rows)

    return context;

def fix_report_coments(index, data) :
    cursor = connection.cursor();
    sql = "UPDATE comentscotent SET isbullying='"+ str(data) +"' WHERE index_='" + str(index)+"'"
    print(sql)
    connection.cursor().execute(sql)

    connection.commit()

def done_learning_coments(nice, bullying) :
    for n in nice:
        insert_dataSet("nice",n[0])
    for b in bullying:
        insert_dataSet("bullying",b[0])
    cursor = connection.cursor();
    sql = "DELETE FROM comentscotent WHERE isbullying=0 or isbullying=2;"
    print(sql)
    connection.cursor().execute(sql)

    connection.commit()

def insert_coments(id, comment, isbullying):
    sql = "INSERT INTO comentscotent (id, coments, isbullying) VALUES ('" + \
          str(id) +"', '" +str(comment) + "', '" + str(isbullying) + "')"
    print("DataSet : " + sql)
    connection.cursor().execute(sql)

    connection.commit()

def select_coments() :
    cursor = connection.cursor();
    sql = "select coments from comentscotent where isbullying=-1 or isbullying=1"
    cursor.execute(sql)

    rows = cursor.fetchall()

    return rows;

def select_coments_dict() :
    cursor = connection.cursor();
    sql = "select * from comentscotent where isbullying=-1 or isbullying=1"
    cursor.execute(sql)
    context = []
    rows = cursor.fetchall()
    for row in rows :
        dic = {'Index':row[0] ,'ID':row[1],'COMENTS':row[2]}
        context.append(dic)
    return context;

def select_report_coments() :
    cursor = connection.cursor();
    sql = "select coments from comentscotent where isbullying=0"
    cursor.execute(sql)

    rows = cursor.fetchall()

    return rows;

def select_bullying_coments() :
    cursor = connection.cursor();
    sql = "select coments from comentscotent where isbullying=2"
    cursor.execute(sql)
    rows = cursor.fetchall()

    return rows;


def select_bullying_all() :
    cursor = connection.cursor();
    sql = "select * from comentscotent where isbullying=2"
    cursor.execute(sql)
    rows = cursor.fetchall()

    return rows;

def select_report_all() :
    cursor = connection.cursor();
    sql = "select * from comentscotent where isbullying=0"
    cursor.execute(sql)

    rows = cursor.fetchall()

    return rows;

def select_bullyindTable():
    cursor = connection.cursor();
    sql = "select coments from bullying"
    cursor.execute(sql)
    # 데이타 Fetch
    rows = cursor.fetchall()

    return rows
