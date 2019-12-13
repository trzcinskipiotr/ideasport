from django.contrib import admin

# Register your models here.
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.models import User
from django.db.models import Q

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

class PlayerFilter(SimpleListFilter):
    title = 'player'
    parameter_name = 'player'

    def lookups(self, request, model_admin):
        players = User.objects.all().order_by('last_name')
        return [(player.id, '{} {}'.format(player.last_name, player.first_name)) for player in players]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(player1__id=self.value()) | Q(player2__id=self.value()))
        else:
            return queryset

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_filter = (PlayerFilter,)
    list_display = ('id', 'round', 'player1', 'player2', 'player1_wo', 'player2_wo', 'mutual_wo', 'set1_player1', 'set1_player2', 'set2_player1', 'set2_player2', 'set3_player1', 'set3_player2')
