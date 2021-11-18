from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import User
import requests

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiemhqMDkyNCIsImEiOiJja3ZnangxdXljMXBlMnBtYTF0c29oN2N3In0.HsgAF-xISYEHuqdLlpJL2A'

DATA_APP = "https://reroot-data-app.herokuapp.com"


def data_api(query, payload=None):
    url = DATA_APP + query
    response = requests.get(url, params=payload)
    print(response)
    return response.json()


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("webapp:profile")
        else:
            return render(request, "webapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "webapp/login.html")


def logout_view(request):
    logout(request)
    return render(request, "webapp/landing.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        # Ensure password matches confirmation
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        if password != confirmation:
            return render(request, "webapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "webapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("webapp:profile")
    else:
        return render(request, "webapp/register.html")


def landing(request):
    return render(request, "webapp/landing.html")


def about(request):
    return render(request, "webapp/about.html")


def questionnaire(request):
    factors_raw = data_api("/factors")
    # print(factors_raw)
    # factors = {"rows": []}
    # per_row = 3

    # for i, key in enumerate(factors_raw.keys()):
    #     row_i, m = divmod(i, per_row)
    #     if m == 0:
    #         factors["rows"].append([key])
    #     else:
    #         factors["rows"][row_i].append(key)

    factors = []
    for k, v in factors_raw.items():
        factors.append({"category": k, "sub_categories": list(v.keys())})
    print(factors)

    return render(request, "webapp/questionnaire.html", {
        "factors": factors[1:],
    })


@login_required(login_url="webapp:login")
def profile(request):
    return render(request, "webapp/profile.html")


def done(request):
    if request.method == "POST":
        factor_names = request.POST.getlist("checkbox")

        # store factors for later use
        if request.user.is_authenticated:
            # TODO store in database
            pass
        else:
            request.session["factors"] = factor_names
        return render(request, "webapp/done.html")
    else:
        return redirect('webapp:questionnaire')


def results(request):
    # TODO Sample Params
    payload = {'opportunity_employment_yes': 1}
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
