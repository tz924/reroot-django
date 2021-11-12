from django.urls import path

from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('log-in', views.log_in, name='log_in'),
    path('log-out', views.log_out, name='log_out'),
    path('register', views.register, name='register'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('questionnaire/importance', views.importance, name='importance'),
    path('questionnaire/question', views.question, name='question'),
    path('questionnaire/choices', views.choices, name='choices'),
    path('questionnaire/done', views.done, name='done'),
    path('results', views.results, name='results'),
    path('profile', views.profile, name='profile'),
    path('city/<str:city>', views.city, name='city'),
]
