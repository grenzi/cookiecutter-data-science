import pyodbc
import csv

def getconn():
    return pyodbc.connect(driver='{SQL Server Native Client 11.0}',server='localhost',database='dddmdb2',trusted_connection='yes')

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

def queryToCsv(sql, filename, include_headers=True):
    f = csv.writer(file(filename, 'wb'))

    cnxn = getconn()
    c = cnxn.cursor()
    c.execute(sql)
    if include_headers:
        f.writerow([d[0] for d in c.description])
    f.writerows(c.fetchall())

