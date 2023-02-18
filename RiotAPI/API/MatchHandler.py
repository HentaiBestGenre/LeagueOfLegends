from .RiotAPI import RiotAPI
import requests
import json


class MatchHandler(RiotAPI):
    def __init__(self, region):
        super().__init__(region)

    def match_info_v5(self, game_id):
        URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
        response = requests.get(URL).json()
        return response

    def match_timeline_v5(self, game_id) -> dict:
        URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}/timeline?api_key={self.token}'
        response = requests.get(URL).json()
        return response

    def user_last_games(self, user_puuid, start=0):
        URL = self.HOST_V5 + f'/lol/match/v5/matches/by-puuid/{user_puuid}/ids?count=10&start={start}&api_key={self.token}'
        response = requests.get(URL).json()
        return response

    def user_stat_in_game(self, game_id, user_name):
        URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
        response = requests.get(URL).json()
        return self.user_game_stat_cleaning(response, user_name)

#   ASYNC
    async def match_info_v5_async(self, game_id):
        URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
        return await self.async_request(URL)

    async def match_timeline_v5_async(self, game_id):
        URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}/timeline?api_key={self.token}'
        return await self.async_request(URL)

    async def user_last_games_async(self, user_puuid, start=0):
        URL = self.HOST_V5 + f'/lol/match/v5/matches/by-puuid/{user_puuid}/ids?count=10&start={start}&api_key={self.token}'
        return await self.async_request(URL)

    async def user_stat_in_game_async(self, game_id, user_name):
        URL = self.HOST_V5 + f'/lol/match/v5/matches/{game_id}?api_key={self.token}'
        response = await self.async_request(URL)

        response = response.content.decode('utf8').replace("'", '"')
        response = json.loads(response)

        return self.user_game_stat_cleaning(response, user_name)

    def user_game_stat_cleaning(self, response, user_name):
        User_game_stat = list(filter(lambda x: x['summonerName'] == user_name, response["info"]["participants"]))[0]
        User_game_stat['gameStartTimestamp'] = response["info"]["gameStartTimestamp"]
        User_game_stat['gameDuration'] = response["info"]["gameDuration"]
        return User_game_stat
