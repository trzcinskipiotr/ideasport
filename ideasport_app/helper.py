from django.contrib.auth.models import User
from django.db import transaction

from ideasport_app.models import Season, League, Round, Match


def copy_league(league_id):
    max_season = Season.objects.all().order_by('order').last()
    old_league = League.objects.get(id=league_id)
    with transaction.atomic():
        new_league = League.objects.create(season=max_season, order=old_league.order, name=old_league.name)
        print('League created.')
        for old_round in old_league.round_set.all():
            new_round = Round.objects.create(league=new_league, order=old_round.order, name=old_round.name, deadline=old_round.deadline)
            print('Round created.')
            for old_match in old_round.match_set.all():
                new_match = Match.objects.create(round=new_round, player1=old_match.player1, player2=old_match.player2)
                print('Match created.')

def replace_user_in_league(league_id, old_user_id, new_user_id):
    league = League.objects.get(id=league_id)
    old_user = User.objects.get(id=old_user_id)
    new_user = User.objects.get(id=new_user_id)
    with transaction.atomic():
        for round in league.round_set.all():
            for match in round.match_set.all():
                if match.player1 == old_user:
                    match.player1 = new_user
                    match.save()
                    print('Match updated.')
                if match.player2 == old_user:
                    match.player2 = new_user
                    match.save()
                    print('Match updated.')
