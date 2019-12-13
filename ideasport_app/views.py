from django.shortcuts import render

from ideasport_app.models import Season, League


def index(request):
    seasons = Season.objects.all()
    context = {'seasons': seasons}
    return render(request, 'index.html', context)

def contact(request):
    seasons = Season.objects.all()
    context = {'seasons': seasons}
    return render(request, 'contact.html', context)

def about(request):
    seasons = Season.objects.all()
    context = {'seasons': seasons}
    return render(request, 'about.html', context)

def league(request, league_id):
    seasons = Season.objects.all()
    league = League.objects.get(id=league_id)
    context = {'seasons': seasons, 'league': league}
    return render(request, 'league.html', context)
