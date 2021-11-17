from django.shortcuts import render, redirect
from . import forms
from .models import City
from .forms import NewUserForm, UserLogInForm
from django.contrib.auth import login, logout
from django.contrib import messages
import requests

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiemhqMDkyNCIsImEiOiJja3ZnangxdXljMXBlMnBtYTF0c29oN2N3In0.HsgAF-xISYEHuqdLlpJL2A'

DATA_APP = "https://reroot-data-app.herokuapp.com"


def data_api(query, payload=None):
    url = DATA_APP + query
    response = requests.get(url, params=payload)
    return response.json()


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
    factors_raw = data_api("/factors")
    factors = {"rows": []}
    per_row = 3

    for i, key in enumerate(factors_raw.keys()):
        row_i, m = divmod(i, per_row)
        if m == 0:
            factors["rows"].append([key])
        else:
            factors["rows"][row_i].append(key)

    return render(request, "webapp/questionnaire.html", {
        "factors": factors,
    })


def question(request):
    if request.method == "POST":
        factor_names = request.POST.getlist("checkbox")

        # store factors for later use
        if request.user.is_authenticated:
            # TODO store in database
            pass
        else:
            request.session["factors"] = factor_names

        factors_raw = data_api("/factors")

        factors = []
        for factor in factor_names:
            temp = {}
            temp["name"] = factor
            temp["choices"] = list(factors_raw[factor].keys())
            factors.append(temp)

        return render(request, "webapp/question.html", {
            "factors": factors,
            "choices": choices
        })
    else:
        return redirect('webapp:questionnaire')


def choices(request):
    return render(request, "webapp/choices.html", {
        "form": forms.NewQuestionnaireForm()
    })


def done(request):
    return render(request, "webapp/done.html", {
        "form": forms.NewQuestionnaireForm()
    })


def results(request):
    payload = {'input_immigrant_language_arabic': 1,
               'input_immigrant_language_chinese': 2}
    scores = data_api("/scores", payload)

    scores_top10 = sorted(scores, key=lambda v: v['score'])[-10:]
    county_codes = [score['county_code'] for score in scores_top10]

    payload = {'counties': ','.join(str(c) for c in county_codes)}
    counties = data_api("/counties", payload)

    for k, v in counties.items():
        v["code"] = k
    counties = list(counties.values())
    print(len(counties))
    for c in counties:
        print(c)

    for c in counties:
        c["longlat"] = [c["county_long"], c["county_lat"]]
        if not c.get("detail"):
            c["detail"] = {}
        for k, v in c.items():
            if k[0] != 'c' and k not in ["longlat", "detail"]:
                c["detail"][k] = v
        for score in scores_top10:
            if c["code"] == str(score["county_code"]):
                c["score"] = round(score["score"] * 10, 2)

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


def compare(request):
    if request.method == "POST":
        county_codes = request.POST.getlist("counties")
        print(request.POST)
        print(county_codes)
        counties_raw = data_api(
            "/counties", {'counties': ','.join(str(c) for c in county_codes)})
        print(counties_raw)
        counties = [v for k, v in counties_raw.items()]

        return render(request, "webapp/compare.html", {
            "counties": counties
        })
    else:
        return render(request, "webapp/compare.html")

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


def profile(request):
    return render(request, "webapp/profile.html")
