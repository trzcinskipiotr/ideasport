from django.urls import path

from ideasport_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('kontakt', views.contact, name='contact'),
    path('onas', views.about, name='about'),
]
