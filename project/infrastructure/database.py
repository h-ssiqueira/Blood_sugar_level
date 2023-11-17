from glob import glob
from pandas import read_csv
from mysql.connector.connection import MySQLConnection

def stablishConnection():
    conn = MySQLConnection(user = 'root',
                          password = 'root',
                          host = '127.0.0.1',
                          database = 'glicemia')
    return conn, conn.cursor()


def importData(cursor):
    files = [f for f in glob("*.csv")]
    for file in files:
        file = read_csv(file, sep=',')
        name = file.Name
        #TODO extract name and check if already inserted
        cursor.execute("""
            SELECT COUNT(*) FROM year WHERE date = ''
        """)
        #TODO if not inserted, insert based on days, then months and them year
        if cursor.fetchone()[0] == 0:
            for row in file:
                cursor.execute("INSERT INTO...")


def mountDatabase(cursor, conn):
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'day'
    """)
    if cursor.fetchone()[0] == 0:
        with open("../data/glicemia.sql", 'r') as script:
            statements = script.read().split(';')
            for statement in statements:
                cursor.execute(statement)
    conn.commit()


conn, cursor = stablishConnection()

mountDatabase(cursor,conn)
importData(cursor)

conn.close()

