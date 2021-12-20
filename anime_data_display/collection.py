import json
import tkinter as tk
from justwatch import JustWatch
import requests as rq

url = "https://graphql.anilist.co/"
query = """query($id: Int){
  Media(id: $id, type: ANIME){
    title {
      romaji
      english
      native
    },
    format,
    description,
    episodes,
    coverImage {
      extraLarge
      large
      medium
    },
    genres,
    tags {
      name,
      rank,
      isMediaSpoiler
    },
    averageScore,
  }
}"""


def collect_seasonal_data(show_id, episodes=0, seasons=1, unaired_seasons=0, movies=0):
    id_var = {"id": show_id}
    sequel_id = None
    query = """query($id: Int){
                 Media(id: $id, type:ANIME){
                   relations{
                     edges{
                       relationType,
                       node{
                         id,
                         episodes,
                         format,
                         status}}}}}"""
    showData = rq.post(url, json={"query": query, "variables": id_var}).json()["data"]["Media"]
    for series in showData["relations"]["edges"]:
        if series["relationType"] == "SEQUEL":
            if series["node"]["format"] in ("TV", "TV_SHORT"):
                if series["node"]["status"] == "FINISHED":
                    episodes += series["node"]["episodes"]
                    seasons += 1
                else:
                    unaired_seasons += 1
            elif series["node"]["format"] == "MOVIE":
                movies += 1
            sequel_id = series["node"]["id"]

    seasonal_data = {
        "total_episodes": episodes,
        "seasons": seasons,
        "unaired_seasons": unaired_seasons,
        "movies": movies,
        "sequel": sequel_id
    }

    if sequel_id:
        seasonal_data = collect_seasonal_data(sequel_id,
                                              episodes=episodes,
                                              seasons=seasons,
                                              unaired_seasons=unaired_seasons,
                                              movies=movies)

    return seasonal_data

if __name__ == "__main__":
    with open("anime_data.json", "r") as anime_data:
        data = json.load(anime_data)

    retry = True
    while retry:
        duplicate = False
        media_id = input("Please input the show's id number. ")
        for show in data:
            if media_id == show["id"]:
                print("We already have that show collected.")
                duplicate = True
        if not duplicate:
            retry = False

    id_var = {"id": media_id}
    request = rq.post(url, json={"query": query, "variables": id_var}).json()['data']["Media"]
    total_episodes, seasons, unaired_seasons, movies, sequel = collect_seasonal_data(media_id, episodes=request["episodes"])

    jared_rating = [0, 0, 0]
    simon_rating = [0, 0, 0]
    kenan_rating = [0, 0, 0]

    print(f"The show is {request['title']['romaji']}, or {request['title']['english']}.")

    jared_rating[0] = int(input("Please input Jared's show rating from 1-100. "))
    jared_rating[1] = int(input("Please input Jared's pacing rating- -50 is slow, 50 is fast. "))
    jared_rating[2] = int(input("Please input Jared's comedy/drama rating. -50 is dramatic, 50 is funny. "))

    if input("Does Simon have available ratings? ").lower() in ("y", "yes"):
        simon_rating[0] = int(input("Please input Simon's show rating from 1-100. "))
        simon_rating[1] = int(input("Please input Simon's pacing rating- -50 is slow, 50 is fast. "))
        simon_rating[2] = int(input("Please input Simon's comedy/drama rating. -50 is dramatic, 50 is funny. "))

    if input("Does Kenan have available ratings? ").lower() in ("y", "yes"):
        kenan_rating[0] = int(input("Please input Kenan's show rating from 1-100. "))
        kenan_rating[1] = int(input("Please input Kenan's pacing rating- -50 is slow, 50 is fast. "))
        kenan_rating[2] = int(input("Please input Kenan's comedy/drama rating. -50 is dramatic, 50 is funny. "))


    entry = {
        "id": media_id,
        "romajiTitle": request["title"]["romaji"],
        "englishTitle": request["title"]["english"],
        "nativeTitle": request["title"]["native"],
        "description": request["description"],
        "episodes": total_episodes,
        "seasons": seasons,
        "unairedSeasons": unaired_seasons,
        "movies": movies,
        "coverLarge": request["coverImage"]["extraLarge"],
        "coverMed": request["coverImage"]["large"],
        "coverSmall": request["coverImage"]["medium"],
        "genres": request["genres"],
        "tags": request["tags"],
        "score": request["averageScore"],
        "jaredScore": jared_rating,
        "simonScore": simon_rating,
        "kenanScore": kenan_rating
    }

    data.append(entry)

    with open("anime_data.json", "w") as anime_data:
        json.dump(data, anime_data, indent=4)
