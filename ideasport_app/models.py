from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from ideasport_app import tennis_utils


class Season(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.name

class League(models.Model):
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    order = models.IntegerField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{} {}'.format(self.season.name, self.name)

class Round(models.Model):
    league = models.ForeignKey(League, on_delete=models.PROTECT)
    order = models.IntegerField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} {} {}'.format(self.league.season.name, self.league.name, self.name)

class Match(models.Model):
    round = models.ForeignKey(Round, on_delete=models.PROTECT)
    player1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='home_match')
    player2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name='away_match')
    player1_wo = models.BooleanField(blank=True, default=False)
    player2_wo = models.BooleanField(blank=True, default=False)
    mutual_wo = models.BooleanField(blank=True, default=False)
    set1_player1 = models.IntegerField(blank=True, null=True)
    set1_player2 = models.IntegerField(blank=True, null=True)
    set2_player1 = models.IntegerField(blank=True, null=True)
    set2_player2 = models.IntegerField(blank=True, null=True)
    set3_player1 = models.IntegerField(blank=True, null=True)
    set3_player2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {} - {} {} (sezon: {})'.format(self.player1.first_name, self.player1.last_name, self.player2.first_name, self.player2.last_name, self.round.league.season.name)

    def is_result_correct(self):
        bools = 0
        if self.player1_wo:
            bools = bools + 1
        if self.player2_wo:
            bools = bools + 1
        if self.mutual_wo:
            bools = bools + 1
        if bools == 0:
            if self.set1_player1 or self.set1_player2 or self.set2_player1 or self.set2_player2 or self.set3_player1 or self.set3_player2:
                set1_correct = tennis_utils.is_set_result_correct(self.set1_player1, self.set1_player2, False)
                set2_correct = tennis_utils.is_set_result_correct(self.set2_player1, self.set2_player2, False)
                set3_correct = tennis_utils.is_set_result_correct(self.set3_player1, self.set3_player2, True)
                print(set1_correct)
                print(set2_correct)
                print(set3_correct)
                if set1_correct and set2_correct and set3_correct:
                    set1_result = tennis_utils.who_win_set(self.set1_player1, self.set1_player2)
                    set2_result = tennis_utils.who_win_set(self.set2_player1, self.set2_player2)
                    set3_result = tennis_utils.who_win_set(self.set3_player1, self.set3_player2)
                    if set1_result == 0 and set2_result == 0 and set3_result == 0:
                        return True
                    if set1_result == 1 and set2_result == 1 and set3_result == 0:
                        return True
                    if set1_result == 2 and set2_result == 2 and set3_result == 0:
                        return True
                    if set1_result == 1 and set2_result == 2 and set3_result == 1:
                        return True
                    if set1_result == 1 and set2_result == 2 and set3_result == 2:
                        return True
                    if set1_result == 2 and set1_result == 1 and set3_result == 2:
                        return True
                    if set1_result == 2 and set2_result == 1 and set3_result == 1:
                        return True
                    return False
                else:
                    return False
            else:
                return True
        elif bools == 1:
            if self.set1_player1 or self.set1_player2 or self.set2_player1 or self.set2_player2 or self.set3_player1 or self.set3_player2:
                return False
            else:
                return True
        else:
            return False

    def save(self, *args, **kwargs):
        super(Match, self).save(*args, **kwargs)
        if not self.is_result_correct():
            raise ValidationError('Nieprawidłowy wynik tenisowy')

    def print_result(self):
        if self.player1_wo:
            return '6:0 6:0 wo'
        if self.player2_wo:
            return '0:6 0:6 wo'
        if self.mutual_wo:
            return 'ob. wo'
        if not self.set1_player1 == None:
            set3_result = tennis_utils.who_win_set(self.set3_player1, self.set3_player2)
            tmp = '{}:{} {}:{}'.format(self.set1_player1, self.set1_player2, self.set2_player1, self.set2_player2)
            if set3_result != 0:
                tmp = '{} {}:{}'.format(tmp, self.set3_player1, self.set3_player2)
            return tmp
        return ''
