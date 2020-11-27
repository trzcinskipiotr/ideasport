from django.urls import path, include

from ideasport_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kontakt/', views.contact, name='contact'),
    path('onas/', views.about, name='about'),
    path('galeria/', views.gallery, name='gallery'),
    path('liga/<int:league_id>/', views.league, name='league'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mojewyniki/', views.myresults, name='myresults'),
    path('wylogowanie/', views.mylogout, name='mylogout'),
    path('zmianahasla/', views.changepass, name='changepass')
]
