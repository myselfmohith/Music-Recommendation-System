IGNORE_KEY = ["spotify_url"]


jsonText = {
    "song_name": "First Thing",
    "spotify_id": "1XtR5oQsad0JY5dJakjGOL",
    "song_art": [
        {
            "height": 640,
            "url": "https://i.scdn.co/image/ab67616d0000b27334457ea0a982ab5876a4d914",
            "width": 640
        },
        {
            "height": 300,
            "url": "https://i.scdn.co/image/ab67616d00001e0234457ea0a982ab5876a4d914",
            "width": 300
        },
        {
            "height": 64,
            "url": "https://i.scdn.co/image/ab67616d0000485134457ea0a982ab5876a4d914",
            "width": 64
        }
    ],
    "artist_names": "Four Tet",
    "spotify_url": "https://open.spotify.com/track/1XtR5oQsad0JY5dJakjGOL",
    "release_date": "2003-03-05",
    "danceability": 0.229,
    "energy": 0.0116,
    "key": 7,
    "loudness": -34.229,
    "mode": 1,
    "speechiness": 0.0358,
    "acousticness": 0.94,
    "instrumentalness": 0.752,
    "liveness": 0.0491,
    "valence": 0.0391,
    "tempo": 80.441
}

columns = ["song_id","song_name","spotify_id","song_art","artist_names","release_date","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo"]
TEMPLATE_STATEMENT_INSERT = "INSERT INTO song_info (%s) VALUES %s;"
TEMPLATE_STATEMENT_INSERT_LAYOUT = "('%s','%s','%s','%s','%s','%s',%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)"
def convert_json_to_set():
    resList = ["ABCFGGHJB"]
    for i,j in jsonText.items():
        if i not in IGNORE_KEY:
            if isinstance(j,str) or isinstance(j,dict) or isinstance(j,list):
                j = str(j).replace('\'','\\\\\'')
                print(j)
            resList.append(j)

    return tuple(resList)

# convert_json_to_set()
print(TEMPLATE_STATEMENT_INSERT % (",".join(columns), TEMPLATE_STATEMENT_INSERT_LAYOUT % convert_json_to_set() ))