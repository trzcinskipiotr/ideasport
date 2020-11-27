from ideasport_app.models import Season

def seasons(request):
    seasons = Season.objects.all()
    return {'seasons': seasons}
