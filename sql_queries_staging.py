import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"


# CREATE TABLES
staging_events_table_create= ("""
CREATE TABLE staging_events (
    artist VARCHAR(MAX),
    auth TEXT,
    firstName TEXT,
    gender CHAR(1),
    itemInSession INT,
    lastName TEXT,
    length DECIMAL(6,2),
    level TEXT,
    location VARCHAR(MAX),
    method TEXT,
    page VARCHAR(300),
    registration FLOAT,
    sessionId INT,
    song VARCHAR(MAX),
    status INT,
    ts BIGINT,
    userAgent VARCHAR(MAX),
    userId TEXT)
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs (
    song_id TEXT,
    num_songs INT,
    title VARCHAR(MAX),
    artist_name VARCHAR(MAX),
    artist_latitude FLOAT,
    year INT,
    duration FLOAT,
    artist_id TEXT,
    artist_longitude FLOAT,
    artist_location VARCHAR(MAX))
""")

# STAGING TABLES
staging_events_copy = ("""
copy staging_events 
from 's3://udacity-dend/log_data/'
credentials 'aws_iam_role={}'
region 'us-west-2'
json 's3://udacity-dend/log_json_path.json'
""").format(config['IAM_ROLE']['ARN'])


staging_songs_copy = ("""
copy staging_songs 
from 's3://udacity-dend/song-data/'
credentials 'aws_iam_role={}'
region 'us-west-2'
json 'auto' truncatecolumns
""").format(config['IAM_ROLE']['ARN'])

                      
# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

