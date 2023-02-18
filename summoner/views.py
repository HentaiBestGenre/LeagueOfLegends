from django.shortcuts import render
import time
import asyncio
from RiotAPI.User import User


async def index(request, region, s_name):
    s = time.time()
    client = User(s_name, region)
    user_data = {
        's_name': s_name,
        'region': region
    }
    rank = client.user_rank()
    task_list = [asyncio.create_task(client.short_stat_in_game_async(game_id)) for game_id in client.user_last_games()]
    last_games_data = list(await asyncio.gather(*task_list))
    print(time.time() - s)
    return render(request, 'summoner/index.html', {'user_data': user_data, 'rank': rank, 'games_data': last_games_data})
