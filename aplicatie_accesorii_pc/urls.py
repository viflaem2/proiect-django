from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('info', views.info, name='info'),
    path('log', views.log, name='log'),
    path('istoric', views.istoric, name='istoric'),
    path('despre', views.despre, name='despre'),
    path('produse', views.afis_produse, name='produse'),
    path('contact', views.contact, name='contact'),
    path('cos_virtual', views.cos_virtual, name='cos_virtual'),
    path('faq', views.faq, name='faq'),
    path('termeni', views.termeni, name='termeni'),
    re_path(r'^accesare(?P<id>\d+)$', views.accesare, name='accesare'),
    re_path(r'^produs/(?P<id>\d+)$', views.afis_produs, name='produs'),
    re_path(r'^categorii/(?P<nume_categorie>[^/]+)$', views.afis_produse, name='categorie'),
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profil', views.profil, name='profil'),
    path('schimba_parola', views.schimba_parola, name='schimba_parola'),
    path('editare_date', views.editare_date, name='editare_date'),
]
