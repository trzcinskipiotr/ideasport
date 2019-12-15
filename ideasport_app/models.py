from functools import cmp_to_key

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from ideasport_app import tennis_utils
from ideasport_app.tennis_utils import compare_by_points_sets_gems


class Season(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(null=True, blank=True, db_index=True)

    def __str__(self):
        return self.name

class League(models.Model):
    season = models.ForeignKey(Season, on_delete=models.PROTECT)
    order = models.IntegerField(null=True, blank=True, db_index=True)
    name = models.CharField(max_length=100)

    def _create_table_from_matches(self, matches):
        scores = {}
        for match in matches:
            id1 = match.player1.id
            id2 = match.player2.id
            for player in [match.player1, match.player2]:
                if not player.id in scores:
                    scores[player.id] = {}
                    scores[player.id]['matches'] = 0
                    scores[player.id]['points'] = 0
                    scores[player.id]['sets_win'] = 0
                    scores[player.id]['sets_lost'] = 0
                    scores[player.id]['sets'] = 0
                    scores[player.id]['gems_win'] = 0
                    scores[player.id]['gems_lost'] = 0
                    scores[player.id]['gems'] = 0
                    scores[player.id]['id'] = player.id
                    scores[player.id]['name'] = '{} {}'.format(player.first_name, player.last_name)
            if match.is_finished():
                scores[id1]['matches'] += 1
                scores[id2]['matches'] += 1
                (points1, points2, sets1_win, sets1_lost, sets2_win, sets2_lost, gems1_win, gems1_lost, gems2_win, gems2_lost) = match.points_sets_gems()
                scores[id1]['points'] += points1
                scores[id2]['points'] += points2
                scores[id1]['sets_win'] += sets1_win
                scores[id1]['sets_lost'] += sets1_lost
                scores[id2]['sets_win'] += sets2_win
                scores[id2]['sets_lost'] += sets2_lost
                scores[id1]['sets'] += (sets1_win - sets1_lost)
                scores[id2]['sets'] += (sets2_win - sets2_lost)
                scores[id1]['gems_win'] += gems1_win
                scores[id1]['gems_lost'] += gems1_lost
                scores[id2]['gems_win'] += gems2_win
                scores[id2]['gems_lost'] += gems2_lost
                scores[id1]['gems'] += (gems1_win - gems1_lost)
                scores[id2]['gems'] += (gems2_win - gems2_lost)
        return scores

    def _sorted_table_by_points(self):
        matches = Match.objects.filter(round__league=self)
        scores = self._create_table_from_matches(matches)
        sorted_table = sorted(scores.values(), key=lambda score: score['points'], reverse=True)
        return sorted_table

    def _split_table_by_points(self, sorted_table_by_points):
        if len(sorted_table_by_points) == 0:
            return []
        splits = []
        current_score = sorted_table_by_points[0]['points']
        current_split = []
        for score in sorted_table_by_points:
            if score['points'] == current_score:
                current_split.append(score)
            else:
                splits.append(current_split)
                current_split = []
                current_split.append(score)
                current_score = score['points']
        if len(current_split) > 0:
            splits.append(current_split)
        return splits

    def _sort_split(self, split):
        if len(split) == 1:
            return split
        player_ids = []
        for score in split:
            player_ids.append(score['id'])
        matches = Match.objects.filter(round__league=self, player1__in=player_ids, player2__in=player_ids)
        scores = self._create_table_from_matches(matches)
        sorted_scores = sorted(scores.values(), key=cmp_to_key(compare_by_points_sets_gems), reverse=True)
        print(sorted_scores)
        new_split = []
        for score in sorted_scores:
            for split_entry in split:
                if split_entry['id'] == score['id']:
                    split_entry['bmatches'] = score['matches']
                    split_entry['bpoints'] = score['points']
                    split_entry['bsets'] = score['sets']
                    split_entry['bsets_win'] = score['sets_win']
                    split_entry['bsets_lost'] = score['sets_lost']
                    split_entry['bgems'] = score['gems']
                    split_entry['bgems_win'] = score['gems_win']
                    split_entry['bgems_lost'] = score['gems_lost']
                    new_split.append(split_entry)
        return new_split

    def _merge_splits(self, splits):
        done_table = []
        place = 1
        for split in splits:
            for score in split:
                score['place'] = place
                done_table.append(score)
                place = place + 1
        return done_table

    def make_table(self):
        sorted_table_by_points = self._sorted_table_by_points()
        splits = self._split_table_by_points(sorted_table_by_points)
        for index, split in enumerate(splits):
            splits[index] = self._sort_split(split)
        done_table = self._merge_splits(splits)
        return done_table

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

    def player1_fullname(self):
        return '{} {}'.format(self.player1.first_name, self.player1.last_name)

    def player2_fullname(self):
        return '{} {}'.format(self.player2.first_name, self.player2.last_name)

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
                    if set1_result == 2 and set2_result == 1 and set3_result == 2:
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

    def is_finished(self):
        if self.player1_wo or self.player2_wo or self.mutual_wo:
            return True
        if self.set1_player1 or self.set1_player2 or self.set2_player1 or self.set2_player2 or self.set3_player1 or self.set3_player2:
            return True
        return False

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

    def points_sets_gems(self):
        points1 = 0
        points2 = 0
        sets1_win = 0
        sets1_lost = 0
        sets2_win = 0
        sets2_lost = 0
        gems1_win = 0
        gems1_lost = 0
        gems2_win = 0
        gems2_lost = 0
        if self.player1_wo:
            points1 = 5
            sets1_win = 2
            gems1_win = 12
            sets2_lost = 2
            gems2_lost = 12
        if self.player2_wo:
            points2 = 5
            sets2_win = 2
            gems2_win = 12
            sets1_lost = 2
            gems1_lost = 12
        set1_result = tennis_utils.who_win_set(self.set1_player1, self.set1_player2)
        set2_result = tennis_utils.who_win_set(self.set2_player1, self.set2_player2)
        set3_result = tennis_utils.who_win_set(self.set3_player1, self.set3_player2)
        if set1_result == 1 and set2_result == 1:
            points1 = 5
            points2 = 1
            sets1_win = 2
            sets2_lost = 2
            gems1_win = self.set1_player1 + self.set2_player1
            gems1_lost = self.set1_player2 + self.set2_player2
            gems2_win = self.set1_player2 + self.set2_player2
            gems2_lost = self.set1_player1 + self.set2_player1
        if set1_result == 2 and set2_result == 2:
            points2 = 5
            points1 = 1
            sets2_win = 2
            sets1_lost = 2
            gems1_win = self.set1_player1 + self.set2_player1
            gems1_lost = self.set1_player2 + self.set2_player2
            gems2_win = self.set1_player2 + self.set2_player2
            gems2_lost = self.set1_player1 + self.set2_player1
        if set3_result == 1:
            points1 = 4
            points2 = 2
            sets1_win = 2
            sets2_win = 1
            sets1_lost = 1
            sets2_lost = 2
            gems1_win = self.set1_player1 + self.set2_player1
            gems1_lost = self.set1_player2 + self.set2_player2
            gems2_win = self.set1_player2 + self.set2_player2
            gems2_lost = self.set1_player1 + self.set2_player1
        if set3_result == 2:
            points2 = 4
            points1 = 2
            sets2_win = 2
            sets1_win = 1
            sets1_lost = 2
            sets2_lost = 1
            gems1_win = self.set1_player1 + self.set2_player1
            gems1_lost = self.set1_player2 + self.set2_player2
            gems2_win = self.set1_player2 + self.set2_player2
            gems2_lost = self.set1_player1 + self.set2_player1
        return (points1, points2, sets1_win, sets1_lost, sets2_win, sets2_lost, gems1_win, gems1_lost, gems2_win, gems2_lost)
