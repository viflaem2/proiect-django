from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('info', views.info, name='info'),
    path('log', views.log, name='log'),
    path('istoric', views.istoric, name='istoric'),
    path('despre', views.despre, name='despre'),
    path('produse', views.produse, name='produse'),
    path('contact', views.contact, name='contact'),
    path('cos_virtual', views.cos_virtual, name='cos_virtual'),
    path('faq', views.faq, name='faq'),
    path('termeni', views.termeni, name='termeni'),
    re_path(r'^accesare(?P<id>\d+)$', views.accesare, name='accesare'),
]
