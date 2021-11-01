from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import forms
from .models import City


def landing(request):
    if request.method == "POST":
        city = request.POST.get("term")
        return redirect("webapp:city", city=city)

    cities = City.objects.all()
    return render(request, "webapp/landing.html", {
        "cities": cities,
    })


def city(request, city):
    return render(request, "webapp/city.html", {'city': city})


def questionnaire(request):
    return render(request, "webapp/questionnaire.html", {
        "form": forms.NewQuestionnaireForm()
    })


def results(request):
    cities = City.objects.all()
    mapbox_access_token = 'pk.eyJ1IjoiemhqMDkyNCIsImEiOiJja3ZnangxdXljMXBlMnBtYTF0c29oN2N3In0.HsgAF-xISYEHuqdLlpJL2A'
    if request.session.get('display') == None:
        request.session['display'] = 5
    if request.method == "POST":
        # form = forms.NewQuestionnaireForm(request.POST)
        # if form.is_valid():
        #     print("valid")
        #     # update
        # else:
        #     # Not possible when all fields required
        #     return render(request, "webapp/results.html")
        if request.POST.get('plus') and request.session['display'] < len(cities):
            request.session['display'] += 1
        if request.POST.get('minus') and request.session['display'] > 0:
            request.session['display'] -= 1
    display = request.session['display']
    return render(request, "webapp/results.html", {
        'cities': cities[:display],
        'mapbox_access_token': mapbox_access_token,
        'display': display})


def profile(request):
    return render(request, "webapp/profile.html")
