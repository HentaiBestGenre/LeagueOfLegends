from django.shortcuts import render, redirect


def index(request):
    if request.method == 'POST':
        return redirect('summoner:index', region=request.POST['region'], s_name=request.POST['summoner_name'])
    return render(request, "main/index.html", {})
