import httpx
import requests
from .RiotConfig import config


class RiotAPI(object):
	"""docstring for RiotAPI"""
	summoners_skills = {
		1: '1',
		2: '2',
		3: 'Exhaust',
		4: 'Flesh',
		5: '5',
		6: 'Ghost',
		7: 'Heal',
		8: '8',
		9: '9',
		10: '10',
		11: 'Smite',
		12: 'Teleport',
		13: '13',
		14: 'Ignite',
		21: 'Barrier'
	}
	languages = {
		'eun1': 'en_US',
		'ru': 'ru_RU',
		'euw1': 'en_US',
		'kr': 'ko_KR',
	}
	regions_v5 = [
		{"region_v5": "americas", "regions": ["la1", "la2", "na1", "br1"]},
		{"region_v5": "asia", "regions": ["jp1", "kr"]},
		{"region_v5": "europe", "regions": ["eun1", "ru", "euw1", "tr1"]},
		{"region_v5": "sea", "regions": ["oc1"]}
	]
	ranks_images = [
		{
			"UNRANKED": 'static/imgs/league-icons-v3/0.png'
		}
	]

	def __init__(self, region):
		self.token = config['token']
		self.region = region
		self.r_v5 = list(filter(lambda x: region.lower() in x["regions"], self.regions_v5))[0]["region_v5"]
		self.HOST = f'https://{region}.api.riotgames.com'
		self.HOST_V5 = f'https://{self.r_v5}.api.riotgames.com'
		self.language = 'en_US'

	@staticmethod
	async def async_request(url):
		async with httpx.AsyncClient() as client:
			response = await client.get(url)
		return response

	def champion(self, champion_name):
		URL = f'https://ddragon.leagueoflegends.com/cdn/12.12.1/data/{self.language}/champion/{champion_name}.json'
		response = requests.get(URL).json()['data']
		return response
