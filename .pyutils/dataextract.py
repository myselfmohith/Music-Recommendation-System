import pandas as pd
import atexit
import os
import logging


# df = pd.read_csv("./triplets_file.csv")
# df2 = pd.read_csv("./song_data.csv")

# # Extract only the song data available in Triplets
# topSongs = df.groupby("song_id").count().reset_index()[["song_id","user_id"]].merge(df2,how="left",on="song_id").sort_values(by=["year","user_id"],ascending=False).drop_duplicates(subset="song_id",keep="first")
# # Build Spotify Search String

# topSongs["search_term_1"] = "track:" + topSongs["title"] + " artist:" + topSongs["artist_name"] + " year:" + topSongs["year"].apply(str)
# topSongs["search_term_2"] = "track:" + topSongs["title"] + " artist:" + topSongs["artist_name"]
# topSongs["status"] = 0
# topSongs["REMARK"] = ""

# # Save the Table for Backup

# topSongs.to_csv("musicinfo.csv",index=False)


# =================================================================
from spotify import find_and_download_spotify_song
from concurrent.futures import ThreadPoolExecutor

csv_file_path = "musicinfo.csv"
if (os.path.exists("musicinfo_checkpoint.csv")):
    csv_file_path = "musicinfo_checkpoint.csv"

musicInfo = pd.read_csv(csv_file_path)
musicInfo["status"] = 0
musicInfo["REMARK"] = ""

executor = ThreadPoolExecutor(60)
count = 0


def onExit():
    print("Stopping and Saving File")
    executor.shutdown(wait=False)
    musicInfo.to_csv("musicinfo_checkpoint.csv", index=False)


atexit.register(onExit)

logging.basicConfig(filename="log-counter.log",filemode="w",format="%(asctime)s %(message)s")
def fetch_data(_, row):
    global count
    try:
        find_and_download_spotify_song(
            row['song_id'], row['search_term_1'], row['search_term_2'])
        row["status"] = 1
    except Exception as e:
        if (str(e.args[0]).split("::")[0].split(" ")[-1] in ["401"]):
            print("==" * 20 + "\n        CHANGE TOKEN\n" + "==" * 20)
            # Stop All Threads
            executor.shutdown(wait=False)
        else:
            row["status"] = 2
            row["REMARK"] = e.args[0]
    finally:
        count += 1
        logging.info("Completed" + str(count))
        musicInfo.loc[_] = row
        if (count % 100 == 0):

            print("saving...")
            musicInfo.to_csv("musicinfo_checkpoint.csv", index=False)

for _, row in musicInfo.iterrows():
    if (row["status"] == 1):
        continue
    executor.submit(fetch_data, _, row)

executor.shutdown(wait=True)
