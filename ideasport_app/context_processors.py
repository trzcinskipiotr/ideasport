from ideasport_app.models import Season

def seasons(request):
    seasons = Season.objects.all()
    current_season = Season.objects.all().order_by('order').last()
    return {'seasons': seasons, 'current_season': current_season}
