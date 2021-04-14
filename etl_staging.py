import configparser
import psycopg2
from sql_queries_staging import copy_table_queries


def load_staging_tables(cur, conn):
    """
    Extracts and copies data from an S3 bucket into the staging tables: staging_events and staging_songs
    --------
    Param:
        cur: Cursor to the Redshift DB.
        conn: Connection to the Redshift DB.
    Return:
        None.
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main function that:
    - Extracts configuration parameters from the dwh.cfg file
    - Connects to the Redshift DB
    - Executes the function that extracts and ingests data to the staging tables
    - Closes connection to the Redshift DB
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()