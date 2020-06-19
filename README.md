# Udacity Data Engineering Nanodegree
# Project 1: Data Modeling with Postgres

This project is a mockup for a fictional music streaming service, Sparkify, which wants to analyze the data they've collected on user activity.  In particular, they are interested in understanding what songs users are listening to and need a way to easily query their JSON logs and song data.  In particular, their focus is on optimizing the database for querying for song play analysis.

# Source Data

The source data is broken into two sets of JSON formatted files:

* log_data: multiple rows identifying songs played on the platform, including information such as artist name, user information, song information, and timestamps
* song_data: one song per file, describing artist and song information

# Database Schema

The database is broken into the following tables:

Fact Table: 

* songplays - records in log data associated with song plays i.e. records with page NextSong: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

Dimension Tables

* users - users in the app: user_id, first_name, last_name, gender, level
* songs - songs in music database: song_id, title, artist_id, year, duration
* artists - artists in music database: artist_id, name, location, latitude, longitude
* time - timestamps of records in songplays broken down into specific units: start_time, hour, day, week, month, year, weekday

The above schema prioritizes the goal of the workflow, analyzing song play analysis, by centering the schema on the songplay fact table.  This tries to minimize the JOIN statements required to analyze data related to song plays.  For example:

* Analyze the number of songplays for each user, or find which users have the most songplays (perhaps needed to understand what drives the most engagement, or similarly finding which users have lower engagement in order to target them with promotional material):
    * This requires no JOIN operations (unless additional user information is desired)
    ````
    SELECT user_id, count(songplay_id)
    FROM songplays
    GROUP BY user_id
    ORDER BY COUNT DESC
    LIMIT 5
    ````
    Result: 
    | user_id | count |
    |--------:|------:|
    |      49 |   689 |
    |      80 |   665 |
    |      97 |   557 |
    |      15 |   463 |
    |      44 |   397 |
    
* Analyze songplay data by time, in order to determine high/low usage periods (perhaps to schedule platform maintenance at off-peak hours, or to know when to provision more resources)
    * This requires no JOIN operations

* Analyze the engagement of users based on their subscription level and city
    * This requires no JOIN operations

While the above sorts of analyses are efficient, some workflows are less efficient than necessary given the current schema.  For example:

* Analyze whether male or female users listen to longer songs in the evening
    * (although a bit contrived) this requires JOINing the users, songs, time, and songplays table, adding considerable work to the query

If these workflows were important and frequent, it might make sense to add redundancy into the database or refactor some tables in order to improve these queries.  This would warrant a tradeoff analysis, however, as additional redundancy adds extra work at data load time, and refactoring could reduce analysis performance of the primary song play queries.
    
# Repository Contents

Included in the repository are:

* raw data files in ./data
* definitions of all sql queries required for table creation, table dropping, and common data insert/select
    * See `sql_queries.py`.  Intent is for this to be imported as utilities by other tools.  Not meant to run standalone
* table creation script which reinitializes the database, removing any existing tables and creating fresh ones
    * `python create_tables.py`
* the etl process, which takes raw data and puts that data into an **existing** db
    * `python etl.py`
* test/debug files
    * test.ipynb: Used as a sandbox for basic query testing/checking of db during development
    * etl.ipynb: Used as a sandbox for developing the etl process before formalizing it in etl.py
