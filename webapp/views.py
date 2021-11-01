from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import forms

cities = ["Paris", "Tokyo", "Shanghai", "NewYorkCity", "London"]


def landing(request):
    if request.method == "POST":
        city = request.POST.get("term")
        return redirect("webapp:city", city=city)

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
    if request.method == "POST":
        form = forms.NewQuestionnaireForm(request.POST)
        if form.is_valid():
            print("valid")
            # update
        else:
            # Not possible when all fields required
            return render(request, "webapp/results.html")
    return render(request, "webapp/results.html")


def profile(request):
    return render(request, "webapp/profile.html")
