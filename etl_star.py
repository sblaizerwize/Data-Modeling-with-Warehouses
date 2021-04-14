import configparser
import psycopg2
from sql_queries_star import insert_table_queries

    
def insert_tables(cur, conn):
    """
    Extracts, transforms and loads data from staging tables into star schema designed tables: time, users, artists, songs, and songplay
    --------
    Param:
        cur: Cursor to the Redshift DB.
        conn: Connection to the Redshift DB.
    Return:
        None.
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

def main():
    """
    Main function that:
    - Extracts configuration parameters from the dwh.cfg file
    - Connects to the Redshift DB
    - Executes the ETL function that ingests data to the star schema tables
    - Closes connection to the Redshift DB
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()