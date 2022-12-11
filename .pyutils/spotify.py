import requests
import os
import json

SONG_MP3_DOWNLOAD_PATH = "./dataset/song-mp3"
SONG_METADATA_DOWNLOAD_PATH = "./dataset/song-metadata"
SPOTIFY_API_KEY = "BQDnl0FF5FY-DaunCVv9dMw_2ZbNxAcPNg59YN5wVE28nFTd8xVY1sC1oCAkNO2UrhW7WjqAxMkITZQhtXeQ5gTUU7Ux2lBwlt2sUwIqUvpLtDXOBs5wj4_TKxg4but5XBsQLCc1iLkzlGTSf7tb0gI6ZMH2F13fJFK7qv8pNRsUaUjxMLtL6TTOqoHNokR6vgw"

SPOTIFY_HEADERS = {
    "Authorization": f"Bearer {SPOTIFY_API_KEY}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def find_and_download_spotify_song(song_id: str, searchQuery1: str, searchQuery2:str = "None"):
    song_save_path = os.path.join(
        SONG_METADATA_DOWNLOAD_PATH, f"{song_id}.json")
    spotify_response = {}
    if os.path.exists(song_save_path):
        return None

    spotify_response = search_in_spotify(searchQuery1)
    if spotify_response == None:
        if searchQuery2 != "None":
            spotify_response = search_in_spotify(searchQuery2)
        if spotify_response == None:
            raise Exception(f"SONG NOT FOUND::search_in_spotify")

    download_spotify_song(song_id, spotify_response["spotify_url"])
    spotify_metadata = download_spotify_metadata(
        spotify_response["spotify_id"])

    # Save Metadata
    tmp_data = open(song_save_path, "w")
    json.dump({**spotify_response, **spotify_metadata}, tmp_data, indent=4)
    tmp_data.close()
    return {**spotify_response, **spotify_metadata}


def download_spotify_song(song_id: str, spotify_link: str):
    song_save_path = os.path.join(SONG_MP3_DOWNLOAD_PATH, f"{song_id}.mp3")
    if os.path.exists(song_save_path):
        return

    response = requests.post(
        url="https://corsproxy.io/?https://api.spotify-downloader.com/",
        data=f"link={spotify_link}",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if (response.status_code != 200):
        raise Exception("SONG FETCH FAILED::download_spotify_song")

    download_link = response.json(
    )["audio"]["url"] if "audio" in response.json() else None
    if (download_link == None):
        raise Exception('DOWNLOAD LINK NOT FOUND::download_spotify_song')

    # Download Song
    print(f"Downloading {spotify_link} -> {song_id}.mp3")
    response = requests.get(download_link)
    if (response.status_code != 200
            or response.headers["Content-Type"] != "application/octet-stream"):
        print(f"Download failed {spotify_link} -> {song_id}.mp3")
        raise Exception("\rSONG DOWNLOAD FAILED::download_spotify_song")

    tmp_file = open(os.path.join(SONG_MP3_DOWNLOAD_PATH, f"{song_id}.mp3"),
                    "wb")
    tmp_file.write(response.content)
    tmp_file.close()

    print(f"Downloaded {spotify_link} -> {song_id}.mp3")


def download_spotify_metadata(spotify_id: str):
    response = requests.get(
        url=f"https://api.spotify.com/v1/audio-features/{spotify_id}",
        headers=SPOTIFY_HEADERS
    )
    if (response.status_code != 200):
        raise Exception(
            f"STATUS CODE {response.status_code}::download_spotify_metadata")

    metadata = response.json()
    if "error" in metadata:
        raise Exception("METADATA ERROR::download_spotify_metadata")
    metadata.pop("type")
    metadata.pop("id")
    metadata.pop("uri")
    metadata.pop("track_href")
    metadata.pop("analysis_url")
    metadata.pop("duration_ms")
    metadata.pop("time_signature")
    return metadata


def search_in_spotify(searchQuery: str):
    response = requests.get(
        url=f"https://api.spotify.com/v1/search?q={searchQuery}&type=track&limit=1",
        headers=SPOTIFY_HEADERS
    )
    if (response.status_code != 200):
        raise Exception(
            f"STATUS CODE {response.status_code}::search_in_spotify")

    resJSON = response.json()
    if "tracks" not in resJSON:
        raise Exception(
            f"TRACKS NOT FOUND IN RESPONSE JSON::search_in_spotify")

    items = resJSON["tracks"]["items"]
    if len(items) < 1:
        return None

    song = items[0]
    returnDict = {}
    returnDict["song_name"] = song["name"]
    returnDict["spotify_id"] = song["id"]
    returnDict["song_art"] = song["album"]["images"] if len(
        song.get("album", {}).get("images", [])) > 0 else []
    returnDict["artist_names"] = "(-)".join(map(lambda x: x["name"],
                                                song["album"]["artists"])) if len(song["album"]["artists"]) > 0 else ""
    returnDict["spotify_url"] = song["external_urls"]["spotify"]
    returnDict["release_date"] = song.get("album", {}).get("release_date", "")

    return returnDict
