from .RiotAPI import RiotAPI
import requests


class UserHandler(RiotAPI):
    def __init__(self, region):
        super().__init__(region)

    def get_user_data(self, user_name):
        URL = self.HOST + f'/lol/summoner/v4/summoners/by-name/{user_name}?api_key={self.token}'
        response = requests.get(URL).json()
        return response

    def get_user_by_puuid(self, puuid):
        URL = self.HOST + f'/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.token}'
        response = requests.get(URL).json()
        return response

    def user_rank(self, user_id):
        URL = self.HOST + f'/lol/league/v4/entries/by-summoner/{user_id}?api_key={self.token}'
        response = requests.get(URL).json()
        return response

    def user_stat_on_champ(self, champ_id, user_id):
        URL = self.HOST + f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{user_id}/by-champion/{champ_id}?api_key={self.token}'
        response = requests.get(URL).json()
        return response

#     ASYNC
    async def get_user_data_async(self, user_name):
        URL = self.HOST + f'/lol/summoner/v4/summoners/by-name/{user_name}?api_key={self.token}'
        return await self.async_request(URL)

    async def get_user_by_puuid_async(self, puuid):
        URL = self.HOST + f'/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.token}'
        return await self.async_request(URL)

    async def user_rank_async(self, user_id):
        URL = self.HOST + f'/lol/league/v4/entries/by-summoner/{user_id}?api_key={self.token}'
        return await self.async_request(URL)

    async def user_stat_on_champ_async(self, champ_id, user_id):
        URL = self.HOST + f'/lol/champion-mastery/v4/champion-masteries/by-summoner/{user_id}/by-champion/{champ_id}?api_key={self.token}'
        return await self.async_request(URL)
