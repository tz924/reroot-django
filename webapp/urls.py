from django.urls import path

from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('log-in', views.log_in, name='log_in'),
    path('log-out', views.log_out, name='log_out'),
    path('register', views.register, name='register'),
    path('about', views.about, name='about'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('done', views.done, name='done'),
    path('results', views.results, name='results'),
    path('compare', views.compare, name='compare'),
    path('profile', views.profile, name='profile'),
]
