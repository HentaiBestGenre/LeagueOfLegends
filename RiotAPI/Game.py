import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .API import MatchHandler
import base64
from io import BytesIO


class Game(MatchHandler):

	def __init__(self, region, match_id):
		super().__init__(region)
		self.time_line = super().match_timeline_v5(match_id)
		self.match_info = super().match_info_v5(match_id)
		summoners = self.match_info['info']['participants']
		self.summonersDataFrame = pd.DataFrame(
			summoners,
			columns=['participantId', 'puuid', 'summonerId', 'summonerName', 'summonerLevel', 'championName', 'teamPosition'],
			index=np.arange(10)+1
		)
		self.match_id = match_id
		self.last_frame = self.time_line['info']['frames'][-1]
		self.game_duration = self.last_frame['timestamp'] / 60000  # in min

	def summoners_stat(self):
		clean_summs_stat = []
		for user_game_data in self.match_info['info']['participants']:
			clean_data = {
				'hero_name': user_game_data["championName"],
				'match_id': self.match_id,
				'scor': {
					'kills': user_game_data['kills'],
					'assists': user_game_data['assists'],
					'deaths': user_game_data['deaths'],
				},
				'champ_data': {
					'participantId': user_game_data['participantId'],
					'champion_name': user_game_data['championName'],
					'position': user_game_data['individualPosition'],
					'champ_icon_url': 'https://ddragon.leagueoflegends.com/cdn/12.14.1/img/champion/{0}.png'.format(user_game_data["championName"])
				},
				'items': [
					f'https://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item0"]}.png',
					f'https://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item1"]}.png',
					f'https://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item2"]}.png',
					f'https://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item3"]}.png',
					f'https://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item4"]}.png',
					f'https://ddragon.leagueoflegends.com/cdn/12.14.1/img/item/{user_game_data["item5"]}.png',
				],
				'summoner_spals': {
					'1': f'{super().summoners_skills[user_game_data["summoner1Id"]]}',
					'2': f'{super().summoners_skills[user_game_data["summoner2Id"]]}'
				}
			}
			clean_summs_stat.append(clean_data)
		return clean_summs_stat

	def graphs(self):
		user_stat = {
			'1': [],
			'2': [],
			'3': [],
			'4': [],
			'5': [],
			'6': [],
			'7': [],
			'8': [],
			'9': [],
			'10': [],
		}
		graphs = {
			'1': {'fight': [], 'farm': []},
			'2': {'fight': [], 'farm': []},
			'3': {'fight': [], 'farm': []},
			'4': {'fight': [], 'farm': []},
			'5': {'fight': [], 'farm': []},
			'6': {'fight': [], 'farm': []},
			'7': {'fight': [], 'farm': []},
			'8': {'fight': [], 'farm': []},
			'9': {'fight': [], 'farm': []},
			'10': {'fight': [], 'farm': []},
		}

		graphs_meta = {
			'farm': {'totalGold': 'Gold', 'minions': 'Minions', 'xp': 'Xp', 'level': 'Level'},
			'fight': {'totalDamageDoneToChampions': 'Damage'}
		}

		timestamp = []
		for frames in self.time_line['info']['frames']:
			timestamp.append(frames['timestamp'] / 60000)
			frame = frames['participantFrames']
			for pId in frame:
				data = frame[pId]
				data.pop('championStats')
				data['totalDamageDoneToChampions'] = data['damageStats']['totalDamageDoneToChampions']
				data.pop('damageStats')
				user_stat[pId].append(data)

		plt.switch_backend('AGG')
		for pId in graphs:
			df = pd.DataFrame(
				user_stat[pId],
				columns=[
					'minionsKilled', 'jungleMinionsKilled',
					'totalGold', 'level',
					'xp', 'totalDamageDoneToChampions'],
				index=timestamp
			)

			graphs[pId]['champion_name'] = self.summonersDataFrame[self.summonersDataFrame.participantId == int(pId)].iloc[0]['championName']

			df['minions'] = df['minionsKilled'] + df['jungleMinionsKilled']
			df = df.drop(columns=['minionsKilled', 'jungleMinionsKilled'])

			for t in graphs_meta:
				for value_type in graphs_meta[t]:
					df[value_type].plot(xlabel='Time', ylabel=graphs_meta[t][value_type], title=graphs_meta[t][value_type])
					graphs[pId][t].append(get_graph())
					plt.close()
		return graphs


def get_graph():
	buffer = BytesIO()
	plt.savefig(buffer, format='png')
	buffer.seek(0)
	image_png = buffer.getvalue()
	graph = base64.b64encode(image_png)
	graph = graph.decode('utf-8')
	buffer.close()
	return graph


name = 'IIIHeNaIII'
game_id = 'RU_404441239'

if __name__ == '__main__':
	client = Game('ru', game_id)
	client.graphs()
	# http://ddragon.leagueoflegends.com/cdn/12.14.1/data/en_US/runesReforged.json
