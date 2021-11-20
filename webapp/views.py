from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import User
import requests

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiemhqMDkyNCIsImEiOiJja3ZnangxdXljMXBlMnBtYTF0c29oN2N3In0.HsgAF-xISYEHuqdLlpJL2A'

DATA_APP = "https://reroot-data-app.herokuapp.com"
IMPORTANT = 1
VERY_IMPORTANT = 2


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
    print(factors_raw)
    factors = []
    for k, v in factors_raw.items():
        factors.append({"category": k, "sub_categories": list(v.keys())})
    print(factors)

    return render(request, "webapp/questionnaire.html", {
        "factors": factors,
    })


@login_required(login_url="webapp:login")
def profile(request):
    user = request.user
    return render(request, "webapp/profile.html", {"user": user})


def done(request):
    if request.method == "POST":
        factor_names = request.POST.getlist("checkbox")

        # store factors for later use
        if request.user.is_authenticated:
            # TODO store in database
            request.session["factors_selected"] = factor_names
        else:
            request.session["factors_selected"] = factor_names
        return render(request, "webapp/done.html")
    else:
        return redirect('webapp:questionnaire')


def get_scores_payload(factors_selected):
    '''
    helper functions
    '''
    factors_raw = data_api("/factors")
    print(factors_raw.values())
    print(factors_selected)
    return {f[k]: 1 for f in factors_raw.values()
            for k in factors_selected if k in f}


def results(request):

    # factors_selected = request.session.get("factors_selected")

    # issues filling out the survey, redo
    # if not factors_selected:
    # return redirect("webapp:questionnaire")

    # payload = get_scores_payload(factors_selected)
    SAMPLE_PAYLOAD = {"diversity_cultural": VERY_IMPORTANT,
                      "service_internet": VERY_IMPORTANT,
                      "environment_air": VERY_IMPORTANT}
    scores = data_api("/scores", SAMPLE_PAYLOAD)

    codes_top10 = sorted(scores, key=lambda c: scores[c]['score'])[-10:]
    print(codes_top10)
    payload = {'counties': ','.join(str(c) for c in codes_top10)}
    counties = data_api("/counties", payload)

    # counties = list(counties.values())

    for c in counties:
        for code in codes_top10:
            if c == code:
                counties[c]['code'] = code
                counties[c]['score'] = scores[code]['score'] * 10
                counties[c]['lnglat'] = counties[c]['coordinates'][::-1]

    counties = list(counties.values())

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

        counties = []
        for code in counties_raw:
            county = {}
            county['code'] = code
            county['name'] = counties_raw[code]['county_name']
            county['rank_details'] = counties_raw[code]['rank_details']
            counties.append(county)

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
