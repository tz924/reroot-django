from django.shortcuts import render, redirect
from . import forms
from .models import City
from .forms import NewUserForm, UserLogInForm
from django.contrib.auth import login, logout
from django.contrib import messages
import requests

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiemhqMDkyNCIsImEiOiJja3ZnangxdXljMXBlMnBtYTF0c29oN2N3In0.HsgAF-xISYEHuqdLlpJL2A'

DATA_APP = "https://reroot-data-app.herokuapp.com"


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


def about(request):
    return render(request, "webapp/about.html")


def city(request, city):
    return render(request, "webapp/city.html",
                  {'city': city,
                   'mapbox_access_token': MAPBOX_ACCESS_TOKEN, })


def questionnaire(request):
    url = DATA_APP + "/parameters"
    response = requests.get(url)
    parameters = response.json()
    factors = {"rows": []}
    per_row = 3

    for i, key in enumerate(parameters.keys()):
        row_i, m = divmod(i, per_row)
        if m == 0:
            factors["rows"].append([key])
        else:
            factors["rows"][row_i].append(key)
    print(factors)

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
    SAMPLE_COUNTIES = [10404, 74002, 1205, 8023, 90364,
                       51023, 98010, 51748]

    url = DATA_APP + "/counties"
    payload = {'counties': ','.join(str(c) for c in SAMPLE_COUNTIES)}
    response = requests.get(url, params=payload)
    print(response.url)
    counties = response.json()
    for k, v in counties.items():
        v["code"] = k
    counties = list(counties.values())
    for c in counties:
        c["longlat"] = [c["county_long"], c["county_lat"]]
        if not c.get("detail"):
            c["detail"] = {}
        for k, v in c.items():
            if k[0] != 'c' and k not in ["longlat", "detail"]:
                c["detail"][k] = v
    # if request.method == "POST":
    # form = forms.NewQuestionnaireForm(request.POST)
    # if form.is_valid():
    #     print("valid")
    #     # update
    # else:
    #     # Not possible when all fields required
    #     return render(request, "webapp/results.html")
    return render(request, "webapp/results.html", {
        'counties': counties,
        'mapbox_access_token': MAPBOX_ACCESS_TOKEN})

# def compare(request):
#     cities = City.objects.all()

#     if request.session.get('display') == None:
#         request.session['display'] = 5
#     if request.method == "POST":
#         # form = forms.NewQuestionnaireForm(request.POST)
#         # if form.is_valid():
#         #     print("valid")
#         #     # update
#         # else:
#         #     # Not possible when all fields required
#         #     return render(request, "webapp/results.html")
#         if request.POST.get('plus') and request.session['display'] < len(cities):
#             request.session['display'] += 1
#         if request.POST.get('minus') and request.session['display'] > 0:
#             request.session['display'] -= 1
#     display = request.session['display']
#     return render(request, "webapp/results.html", {
#         'cities': cities[:display],
#         'mapbox_access_token': MAPBOX_ACCESS_TOKEN,
#         'display': display})


def profile(request):
    return render(request, "webapp/profile.html")
