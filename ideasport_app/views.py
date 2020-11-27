from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.shortcuts import render

from ideasport_app.mail_utils import send_mail
from ideasport_app.models import Season, League, Gallery, Match


def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def gallery(request):
    galleries = Gallery.objects.all().order_by('order')
    context = {'galleries': galleries}
    return render(request, 'gallery.html', context)

def league(request, league_id):
    league = League.objects.get(id=league_id)
    table = league.make_table()
    context = {'league': league, 'table': table}
    return render(request, 'league.html', context)

def myresults(request):
    context = {}
    if request.user.is_authenticated:
        last_season = Season.objects.order_by('-order').last()
        matches = Match.objects.filter(round__league__season=last_season).filter(Q(player1=request.user) | Q(player2=request.user))
        context = {'matches': matches, 'last_season': last_season}
        if request.method == 'POST':
            matches = Match.objects.filter(id=request.POST['matchid'])
            if matches.count() == 1:
                match = matches[0]
                if len(match.print_result()) == 0:
                    if (match.player1 == request.user) or (match.player2 == request.user):
                        if (request.POST['set1_player1'].strip().isdigit()) and (request.POST['set1_player2'].strip().isdigit()) and (request.POST['set2_player1'].strip().isdigit()) and (request.POST['set2_player2'].strip().isdigit()):
                            if (len(request.POST['set3_player1'].strip()) == 0 and len(request.POST['set3_player2'].strip()) == 0) or (len(request.POST['set3_player1'].strip()) > 0 and len(request.POST['set3_player2'].strip()) > 0 and request.POST['set2_player1'].strip().isdigit() and request.POST['set2_player2'].strip().isdigit()):
                                match.set1_player1 = int(request.POST['set1_player1'].strip())
                                match.set1_player2 = int(request.POST['set1_player2'].strip())
                                match.set2_player1 = int(request.POST['set2_player1'].strip())
                                match.set2_player2 = int(request.POST['set2_player2'].strip())
                                if len(request.POST['set3_player1'].strip()) > 0:
                                    match.set3_player1 = int(request.POST['set3_player1'].strip())
                                if len(request.POST['set3_player2'].strip()) > 0:
                                    match.set3_player2 = int(request.POST['set3_player2'].strip())
                                if match.is_result_correct():
                                    match.save()
                                    send_mail(request, match)
                                    context['success'] = 'Wynik meczu {} - {} zapisany: {}.'.format(match.player1_fullname(), match.player2_fullname(), match.print_result())
                                else:
                                    context['error'] = 'Wpisz poprawny wynik meczu.'
                            else:
                                context['error'] = 'Wpisz poprawny wynik meczu.'
                        else:
                            context['error'] = 'Wpisz poprawny wynik meczu.'
                    else:
                        context['error'] = 'Nie możesz uzupełniać wyników meczy w których nie grasz.'
                else:
                    context['error'] = 'Wynik meczu jest już wpisany.'
            else:
                context['error'] = 'Nie można odnaleźć meczu.'
    return render(request, 'myresults.html', context)


def mylogout(request):
    return render(request, 'logout.html')

def changepass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if not (request.POST['password1'] and request.POST['password2'] and request.POST['password1'] == request.POST['password2']):
                return render(request, 'changepass.html', {'error': 'Hasła nie są takie same.'})
            if len(request.POST['password1']) < 8:
                return render(request, 'changepass.html', {'error': 'Podane hasło jest za krótkie.'})
            request.user.set_password(request.POST['password1'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            return render(request, 'changepass.html', {'success': 'Hasło zostało zmienione.'})
        return render(request, 'changepass.html')
    else:
        return render(request, 'changepass.html', {'error': 'Strona tylko dla zalogowanych użytkowników.'})
