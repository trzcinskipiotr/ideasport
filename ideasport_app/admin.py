from django import forms
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
        players = User.objects.exclude(first_name__exact='').order_by('last_name')
        return [(player.id, '{} {}'.format(player.last_name, player.first_name)) for player in players]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(player1__id=self.value()) | Q(player2__id=self.value()))
        else:
            return queryset


class UserFullNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} {}".format(obj.last_name, obj.first_name)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_filter = (PlayerFilter,)
    list_display = ('id', 'round', 'player1_fullname', 'player2_fullname', 'player1_wo', 'player2_wo', 'mutual_wo', 'set1_player1', 'set1_player2', 'set2_player1', 'set2_player2', 'set3_player1', 'set3_player2')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "player1" or db_field.name == "player2":
            return UserFullNameChoiceField(User.objects.exclude(first_name__exact='').order_by('last_name'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
