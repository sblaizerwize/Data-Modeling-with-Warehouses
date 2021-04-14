import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
time_table_create = ("""
CREATE TABLE time (
    start_time TIMESTAMP PRIMARY KEY NOT NULL,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday TEXT)
""")

user_table_create = ("""
CREATE TABLE users (
    user_id INT PRIMARY KEY NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    level TEXT)
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id TEXT PRIMARY KEY NOT NULL,
    name TEXT,
    location TEXT,
    latitude FLOAT,
    longitude FLOAT)
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id TEXT PRIMARY KEY NOT NULL,
    title TEXT,
    artist_id TEXT NOT NULL REFERENCES artists(artist_id),
    year INT,
    duration DECIMAL(6,2))
""")

songplay_table_create = ("""
CREATE TABLE songplay (
    songplay_id INT IDENTITY(1,1) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL REFERENCES time(start_time),
    user_id INT,
    level TEXT,
    song_id TEXT NOT NULL REFERENCES songs(song_id),
    artist_id TEXT NOT NULL REFERENCES artists(artist_id),
    session_id INT,
    location TEXT,
    user_agent TEXT)
""")

# FINAL TABLES
time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT 
    ts AS start_time,
    EXTRACT(hour FROM ts) AS hour,
    EXTRACT(day FROM ts) AS day,
    EXTRACT(week FROM ts) AS week,
    EXTRACT(month FROM ts) AS month,
    EXTRACT(year FROM ts) AS year,
    CASE EXTRACT(dow FROM ts)
        WHEN 1 THEN 'Sunday'
        WHEN 2 THEN 'Monday'
        WHEN 3 THEN 'Tuesday'
        WHEN 4 THEN 'Wednesday'
        WHEN 5 THEN 'Thursday'
        WHEN 6 THEN 'Friday'
        ELSE 'Saturday'
    END AS weeday
FROM (
    SELECT (TIMESTAMP 'epoch' + st.ts/1000 * INTERVAL '1 second') AS ts
    FROM staging_events st)
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT  
        DISTINCT (nuser.userId :: integer),
        nuser.firstname,
        nuser.lastname,
        nuser.gender,
        nuser.level
    FROM (
        SELECT
            CASE 
                WHEN st.userId != ' ' THEN st.userId
                ELSE NULL
            END AS userId,
            st.firstname,
            st.lastname,
            st.gender,
            st.level,
            st.page
        FROM staging_events st) AS nuser
    WHERE nuser.userId IS NOT NULL
    AND nuser.page = 'NextSong'
""")
                      
artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT 
        DISTINCT sts.artist_id,
        sts.artist_name,
        sts.artist_location,
        sts.artist_latitude,
        sts.artist_longitude    
    FROM staging_songs sts
""")
                      
song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT
        DISTINCT sto.song_id,
        sto.title,
        sto.artist_id,
        sto.year,
        sto.duration
    FROM staging_songs sto
""")
                      
songplay_table_insert = ("""
    INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT
        TIMESTAMP 'epoch' + st.ts/1000 * INTERVAL '1 second' AS start_time,
        st.userId :: integer AS user_id,
        st.level AS level,
        sa.song_id AS song_id,
        sa.artist_id AS artist_id,
        st.sessionId AS session_id,
        st.location AS location,
        st.userAgent AS user_agent   
    FROM staging_events st
    JOIN (
        SELECT
            s.song_id,
            a.artist_id,
            s.duration,
            s.title,
            a.name
        FROM songs s
        JOIN artists a
        ON s.artist_id = a.artist_id) AS sa
    ON
        (st.length = sa.duration AND
         st.song = sa.title AND
         st.artist = sa.name)
    WHERE st.page = 'NextSong';
""")
                      
# QUERY LISTS

create_table_queries = [time_table_create, user_table_create, artist_table_create, song_table_create, songplay_table_create]

drop_table_queries = [songplay_table_drop, song_table_drop, artist_table_drop, user_table_drop, time_table_drop]

insert_table_queries = [time_table_insert, user_table_insert, artist_table_insert, song_table_insert, songplay_table_insert]
