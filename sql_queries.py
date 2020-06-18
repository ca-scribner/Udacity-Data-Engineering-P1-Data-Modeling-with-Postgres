# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
    songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    user_id INT,
    level VARCHAR,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INT,
    location VARCHAR,
    user_agent VARCHAR
)
""")

user_table_create = ("""
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    gender CHAR(1),
    level VARCHAR
)
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id VARCHAR PRIMARY KEY,
    title VARCHAR,
    artist_id VARCHAR,
    year INT,
    duration FLOAT
)
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    location VARCHAR,
    latitude VARCHAR,
    longtitude VARCHAR
)
""")

time_table_create = ("""
CREATE TABLE time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday INT
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

# On conflict, update the user's info and assume the newest is correct
user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id)
DO UPDATE SET 
    user_id=EXCLUDED.user_id,
    first_name=EXCLUDED.first_name,
    last_name=EXCLUDED.last_name,
    gender=EXCLUDED.gender,
    level=EXCLUDED.level
""")

# On conflict, update the song's info and assume the newest is correct
song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO UPDATE SET
    song_id=EXCLUDED.song_id,
    title=EXCLUDED.title,
    artist_id=EXCLUDED.artist_id,
    year=EXCLUDED.year,
    duration=EXCLUDED.duration
""")

# On conflict, update the artist's info and assume the newest is correct
artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longtitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO UPDATE SET
    artist_id=EXCLUDED.artist_id,
    name=EXCLUDED.name,
    location=EXCLUDED.location,
    latitude=EXCLUDED.latitude,
    longtitude=EXCLUDED.longtitude
""")

# On conflict, ignore collision because timestamps should not be mutable
# Correcting a poor timestamp would be done with a different query
time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time)
DO NOTHING
""")

# FIND SONGS

song_select = ("""
SELECT songs.song_id, artists.artist_id FROM songs
JOIN artists on songs.artist_id=artists.artist_id
WHERE songs.title=%s
AND   artists.name=%s
AND   songs.duration=%s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]