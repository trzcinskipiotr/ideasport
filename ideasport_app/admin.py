from django.contrib import admin

# Register your models here.
from ideasport_app.models import Season, League, Round, Match


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order')

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'season')

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'order', 'deadline', 'league')

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'round', 'player1', 'player2', 'player1_wo', 'player2_wo', 'mutual_wo', 'set1_player1', 'set1_player2', 'set2_player1', 'set2_player2', 'set3_player1', 'set3_player2')
