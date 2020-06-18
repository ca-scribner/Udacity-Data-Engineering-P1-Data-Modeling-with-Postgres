# Applies the ETL process for loading song and log data to the database

import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Processes a song file, loading data into songs and artists tables
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    songs_columns = ["song_id", "title", "artist_id", "year", "duration"]
    song_data = df[songs_columns].values[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_columns = ["artist_id",
                      "artist_name",
                      "artist_location",
                      "artist_latitude",
                      "artist_longitude",
                     ]
    artist_data = df[artist_columns].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Process a log file, loading data into the time, songplays, and users tables
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == "NextSong"]

    # convert timestamp column to datetime
    df['ts_as_datetime'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = {
        'timestamp': df['ts_as_datetime'],
        'hour': df['ts_as_datetime'].dt.hour,
        'day': df['ts_as_datetime'].dt.day, 
        'week': df['ts_as_datetime'].dt.week, 
        'month': df['ts_as_datetime'].dt.month, 
        'year': df['ts_as_datetime'].dt.year, 
        'weekday': df['ts_as_datetime'].dt.weekday,
    }
    column_labels = list(time_data.keys())
    time_df = pd.DataFrame(data=time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_columns = ["userId", "firstName", "lastName", "gender", "level"]
    user_df = df[user_columns]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            # Adding songplay as an unknown song/artist
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts_as_datetime,
                         row.userId,
                         row.level,
                         songid,
                         artistid,
                         row.sessionId,
                         row.location,
                         row.userAgent
                        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Finds all JSON files in a directory and its children and processes with a provided func
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()