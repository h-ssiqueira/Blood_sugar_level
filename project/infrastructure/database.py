from datetime import datetime
from glob import glob
import logging
from mysql.connector.connection import MySQLConnection
from os.path import basename,dirname,realpath
from pandas import read_csv

def stablishConnection():
    conn = MySQLConnection(user = 'root',
                           password = 'root',
                           host = '127.0.0.1',
                           database = 'glicemia')
    logging.info("Connection to database stablished.")
    return conn, conn.cursor()

def mountDatabase(cursor, conn, dataDir):
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'blood_sugar_level'
    """)
    if cursor.fetchone()[0] == 0:
        logging.info("Creating table blood_sugar_level.")
        with open(''.join([dataDir,"bloodSugarLevelTable.sql"]), 'r') as script:
            statements = script.read().split(';')
            for statement in statements:
                cursor.execute(statement)
        conn.commit()
        logging.info("Table blood_sugar_level created successfully.")


def importData(cursor,conn,dataDir):
    files = [f for f in glob(''.join([dataDir,'*.csv']))]
    logging.info(f"{len(files)} csv files found. Importing data.")
    for file in files:
        year = basename(file).replace(".csv",'')
        cursor.execute("SELECT COUNT(*) FROM blood_sugar_level WHERE YEAR(date) = " + year)
        if cursor.fetchone()[0] == 0:
            logging.info(f"Inserting data from year: {year}.")
            file = read_csv(file, sep=',')
            print(file.head())
            for _, row in file.iterrows():
                parsed_date = datetime.strptime(row['Date'], "%a. %d/%b.")
                cursor.execute("""
                    INSERT INTO blood_sugar_level
                    (date, breakfast, after_breakfast, lunch, after_lunch, dinner, after_dinner, extra, comment)
                    VALUES (STR_TO_DATE(%s, '%Y-%m-%d'), %s, %s, %s, %s, %s, %s, %s, %s);
                """, (f"{year}-{parsed_date.month}-{parsed_date.day}", row['Before breakfast'], row['2h after breakfast'], row['Before lunch'], row['2h after lunch'], row['Before dinner'], row['2h after dinner'], row['Extra'], row['Comment']))
            conn.commit()
            logging.info(f"Data from year {year} inserted successfully.")
        else:
            logging.info(f"Data from year {year} already imported.")

def updateViews(cursor,conn,dataDir):
    logging.info("Updating views.")
    with open(''.join([dataDir,"views.sql"]), 'r') as script:
        statements = script.read().split(';')
        for statement in statements:
            cursor.execute(statement)
    conn.commit()
    logging.info("Views updated successfully.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dataDir = dirname(realpath(__file__)).replace("project/infrastructure","data/")
    conn, cursor = stablishConnection()
    mountDatabase(cursor,conn,dataDir)
    importData(cursor,conn,dataDir)
    updateViews(cursor,conn,dataDir)
    conn.close()

