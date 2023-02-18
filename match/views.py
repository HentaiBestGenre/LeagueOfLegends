from django.shortcuts import render
import time
from RiotAPI.Game import Game


def index(request, match_id):
    s = time.time()
    client = Game(match_id.split('_')[0].lower(), match_id)
    clean_stat = client.summoners_stat()
    graphs = client.graphs()
    print(time.time() - s)
    # , 'graphs': graphs
    game_gen_data = {}
    return render(request, 'match/index.html', {'game_gen_data': game_gen_data, 'clean_stat': clean_stat, 'graphs': graphs})
