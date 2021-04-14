import configparser
import psycopg2
from sql_queries_star import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops, if exist, the star schema tables: time, users, artists, songs, and songplay
    --------
    Param:
        cur: Cursor to the Redshift DB.
        conn: Connection to the Redshift DB.
    Return:
        None.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates the star schema tables: time, users, artists, songs, and songplay
    --------
    Param:
        cur: Cursor to the Redshift DB.
        conn: Connection to the Redshift DB.
    Return:
        None.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Main function that:
    - Extracts configuration parameters from the dwh.cfg file
    - Connects to the Redshift DB
    - Executes the functions to drop and create star schema tables
    - Closes the connection to the Redshift DB
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()