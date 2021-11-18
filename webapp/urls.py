from django.urls import path

from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('about', views.about, name='about'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('done', views.done, name='done'),
    path('results', views.results, name='results'),
    path('compare', views.compare, name='compare'),
    path('profile', views.profile, name='profile'),
]
