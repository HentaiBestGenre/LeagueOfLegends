from .API import UserHandler, MatchHandler
import datetime as dt
import requests
# from API import UserHandler, MatchHandler


class User(UserHandler, MatchHandler):
    """docstring for User"""

    def __init__(self, user_name, region):
        super(UserHandler, self).__init__(region=region)
        super(MatchHandler, self).__init__(region=region)
        user_data = super().get_user_data(user_name)
        self.user_data = user_data
        self.id = user_data['id']
        self.accountId = user_data['accountId']
        self.puuid = user_data['puuid']
        self.name = user_data['name']

    def __str__(self):
        return f'name: {self.name}\nid: {self.id}\naccountId: {self.accountId}\npuuid: {self.puuid}'

    # user statistic and other general data

    def user_rank(self, **kwargs):
        return super().user_rank(self.id)[0]

    def user_stat_on_champ(self, champ_id, **kwargs):
        return super().user_stat_on_champ(champ_id, self.id)

    # matches info
    def match_info_v5(self, match_id):
        return super().match_info_v5(match_id)

    def match_timeline_v5(self, match_id):
        return super(MatchHandler).match_timeline_v5(match_id)

    def user_last_games(self, **kwargs):
        return super().user_last_games(self.puuid)

    def user_stat_in_game(self, match_id, **kwargs):
        return super().user_stat_in_game(match_id, self.name)

    def short_stat_in_game(self, match_id):
        user_game_data = super().user_stat_in_game(match_id, self.name)
        return self.short_stat_data_cleaning(user_game_data, match_id)

    def short_stat_data_cleaning(self, game_data, match_id):
        kda = lambda x, y, z: round((x+y)/z, 1) if z != 0 else round((x+y)/(z+1), 1)
        return {
            'match_id': match_id,
            'team_id': game_data["teamId"],
            'game_duration': dt.datetime.fromtimestamp(game_data['gameDuration']),
            'ago': dt.datetime.fromtimestamp(game_data['gameStartTimestamp']/1000),
            'score': {
                'kills': game_data['kills'],
                'assists': game_data['assists'],
                'deaths': game_data['deaths'],
                'kda': kda(game_data["assists"], game_data["kills"], game_data['deaths'])
            },
            'champ_data': {
                'champion_name': game_data['championName'],
                'position': game_data['individualPosition'],
                'champ_icon_url': 'https://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/{0}.png'.format(
                    game_data["championName"])
            },
            'items': [f'https://ddragon.leagueoflegends.com/cdn/13.3.1/img/item/{game_data[f"item{i}"]}.png' for i
                      in range(6)],
            'summoner_spells': {
                '1': f'{super().summoners_skills[game_data["summoner1Id"]]}',
                '2': f'{super().summoners_skills[game_data["summoner2Id"]]}'
            },
            "win": game_data["win"]
        }

    @staticmethod
    def activeplayer_data_local():
        URL = f"https://127.0.0.1:2999/liveclientdata/activeplayer"
        respons = requests.get(URL, verify=False).json()
        return respons

    # ASYNC
    # user statistic and other general data

    async def user_rank_async(self, **kwargs):
        return await super().user_rank_async(self.id)

    async def user_stat_on_champ_async(self, champ_id, **kwargs):
        return await super().user_stat_on_champ_async(champ_id, self.id)

    # async matchs info
    async def match_info_v5_async(self, game_id):
        return await super().match_info_v5_async(game_id)

    async def matche_timeline_v5_async(self, game_id):
        return await super().match_timeline_v5_async(game_id)

    async def user_last_games_async(self, **kwargs):
        return await super().user_last_games_async(self.puuid)

    async def user_stat_in_game_async(self, game_id, **kwargs):
        return await super().user_stat_in_game_async(game_id, self.name)

    async def short_stat_in_game_async(self, match_id):
        user_game_data = await super().user_stat_in_game_async(match_id, self.name)
        return self.short_stat_data_cleaning(user_game_data, match_id)


if __name__ == "__main__":
    c = User("IIIHeNaIII", "RU")
    c.short_stat_in_game("RU_427710121")
