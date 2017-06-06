def getconn():
    return pyodbc.connect(driver='{SQL Server Native Client 11.0}',server='localhost\SQL2014',database='dddmdb',trusted_connection='yes')

def queryToDict(sql):
    res=[]
    connection = getconn()
    cursor = connection.cursor()
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    for row in cursor.fetchall():
        res.append(dict(zip(columns, row)))
    connection.close()
    return res
