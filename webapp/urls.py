from django.urls import path

from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('questionnaire', views.questionnaire, name='questionnaire'),
    path('results', views.results, name='results'),
    path('profile', views.profile, name='profile'),
    path('city/<str:city>', views.city, name='city'),
]
