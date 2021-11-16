from django.shortcuts import render, redirect
from . import forms
from .models import City
from .forms import NewUserForm, UserLogInForm
from django.contrib.auth import login, logout
from django.contrib import messages

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiemhqMDkyNCIsImEiOiJja3ZnangxdXljMXBlMnBtYTF0c29oN2N3In0.HsgAF-xISYEHuqdLlpJL2A'


def log_in(request):
    if request.method == "POST":
        form = UserLogInForm(request.POST)
        if form.is_valid():
            print("form valid")
            login(request, request.user)
            messages.success(request, "Log in successful.")
            return redirect("webapp:profile")
        print("form not valid")
        messages.error(
            request, "Unsuccessful log in. Invalid information.")

    # if request.method is GET
    form = UserLogInForm()
    return render(request=request, template_name="webapp/log_in.html", context={"log_in_form": form})


def log_out(request):
    logout(request)
    return render(request, "webapp/log_out.html", {
    })


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            print("form valid")
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("webapp:log_in")
        print("form not valid")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    # if request.method is GET
    form = NewUserForm()
    return render(request=request, template_name="webapp/register.html", context={"register_form": form})


def landing(request):
    if request.method == "POST":
        city = request.POST.get("term")
        return redirect("webapp:city", city=city)

    cities = City.objects.all()
    return render(request, "webapp/landing.html", {
        "cities": cities,
    })


def city(request, city):
    return render(request, "webapp/city.html",
                  {'city': city,
                   'mapbox_access_token': MAPBOX_ACCESS_TOKEN, })


def questionnaire(request):
    factors = {
        "row1": ["disability", "diversity", "affordability"],
        "row2": ["public transit", "education", "clean water"],
        "row3": ["wages", "language", "lgbt", "defund police"],
        "row4": ["childcare", "voting", "medical"]
    }
    return render(request, "webapp/questionnaire.html", {
        "factors": factors,
        "form": forms.NewQuestionnaireForm()

    })


def question(request):
    return render(request, "webapp/question.html", {
        "form": forms.NewQuestionnaireForm()
    })


def choices(request):
    return render(request, "webapp/choices.html", {
        "form": forms.NewQuestionnaireForm()
    })


def done(request):
    return render(request, "webapp/done.html", {
        "form": forms.NewQuestionnaireForm()
    })


def results(request):
    cities = City.objects.all()

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
        'mapbox_access_token': MAPBOX_ACCESS_TOKEN,
        'display': display})


def profile(request):
    return render(request, "webapp/profile.html")
