create database music_recsys;

create table song_info(
    song_index serial primary key,
    song_id varchar(100) unique not null,
    song_name varchar(255) not null,
    spotify_id varchar(100) unique not null,
    song_art text,
    artist_names varchar(255) not null,
    release_date Date,
    danceability Numeric(8,6) default 0,
    energy Numeric(8,6) default 0,
    key Numeric(8,6) default 0,
    loudness Numeric(8,6) default 0,
    mode Numeric(8,6) default 0,
    speechiness Numeric(8,6) default 0,
    acousticness Numeric(8,6) default 0,
    instrumentalness Numeric(8,6) default 0,
    liveness Numeric(8,6) default 0,
    valence Numeric(8,6) default 0,
    tempo Numeric(8,6) default 0
);