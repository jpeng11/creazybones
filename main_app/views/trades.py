from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from main_app.models import Crazybone, TradeRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main_app.forms import TradeSearchForm

from ..forms import TradeSearchForm

@login_required
def index(req):
    return render(req, 'trades/form.html', {'form':TradeSearchForm})

@login_required
def result(req):
    user_crazybones = req.user.profile.cb.all()
    print(user_crazybones)

    search_method = req.GET['search_method']
    search_query = req.GET['search_query'].strip()

    if search_method == "cb_name":
        try:
            crazybone = Crazybone.objects.get(name__iexact=search_query)
            profiles = crazybone.profile_set.all()
            if(len(profiles) != 0):
                results = []
                for profile in profiles:
                    results.append({
                        "user": profile.user.username,
                        "cb": crazybone.name
                    })
            else:
                results = "No user has that Crazy Bone yet."
        except:
            results = None
    else:
        try:
            user = User.objects.get(username__iexact=search_query)
            crazybones = User.objects.get(username__iexact=search_query).profile.cb.all()
            results = []
            for crazybone in crazybones:
                results.append({
                    "user": search_query,
                    "cb": crazybone.name
                })
        except:
            results = None

    return render(req, 'trades/results.html', {'results': results, 'user_crazybones':user_crazybones, 'search_method':search_method})

@login_required
def create(req):
    selected_values = req.POST['selected'].split('-')
    print(selected_values)
    try:
        new_user_from = req.user.profile
        new_user_to = User.objects.get(username__iexact=selected_values[0]).profile
        new_cb_offered = new_user_from.cb.get(name__iexact=req.POST['offered'])
        new_cb_wanted = new_user_to.cb.get(name__iexact=selected_values[1])
        new_trade = TradeRequest.objects.create(user_from=new_user_from, user_to=new_user_to, cb_wanted=new_cb_wanted, cb_offered=new_cb_offered)
        return HttpResponse("<h1> Trade Created - See Admin Page for Now </h1>")
    except Exception as err:
        print(err)
        return HttpResponse("Something went wrong")