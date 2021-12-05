import json
import requests as rq


def collect_seasonal_data(show_id, episodes=0, seasons=1):
    id_var = {"id": show_id}
    sequel_id = None
    query = """query($id: Int){
                 Media(id: $id, type:ANIME){
                   relations{
                     edges{
                       relationType,
                       node{
                         id,
                         episodes}}}}}"""
    showData = rq.post(url, json={"query": query, "variables": id_var}).json()["data"]["Media"]
    for series in showData["relations"]["edges"]:
        if series["relationType"] == "SEQUEL":
            episodes += series["node"]["episodes"]
            seasons += 1
            sequel_id = series["node"]["id"]

    if sequel_id:
        episodes, seasons, sequel_id = collect_seasonal_data(sequel_id, episodes=episodes, seasons=seasons)

    return episodes, seasons, sequel_id


url = "https://graphql.anilist.co/"
media_id = input("Please input the show's id number. ")

id_var = {"id": media_id}

query = """query($id: Int){
  Media(id: $id, type: ANIME){
    title {
      romaji
      english
      native
    },
    description,
    episodes,
    relations {
      edges {
        node {
          title {
            romaji,
            english
          }
          id,
          episodes,
        },
        relationType
      }
    },
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

request = rq.post(url, json={"query": query, "variables": id_var}).json()['data']["Media"]

# for field in request:
#     print(field, request[field])

# for series in request["relations"]["edges"]:
#     print(series)

total_episodes, seasons, sequel = collect_seasonal_data(media_id, episodes=request["episodes"])

entry = {
    "romajiTitle": request["title"]["romaji"],
    "englishTitle": request["title"]["english"],
    "nativeTitle": request["title"]["native"],
    "description": request["description"],
    "episodes": total_episodes,
    "seasons": seasons,
    "coverLarge": request["coverImage"]["extraLarge"],
    "coverMed": request["coverImage"]["large"],
    "coverSmall": request["coverImage"]["medium"],
    "genres": request["genres"],
    "tags": request["tags"],
    "score": request["averageScore"]
}

print(entry)
