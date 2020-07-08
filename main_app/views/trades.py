from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main_app.models import Crazybone, TradeRequest, Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main_app.forms import TradeSearchForm


@login_required
def index(req):
    return render(req, 'trades/form.html', {'form':TradeSearchForm, 'error':None})

@login_required
def result(req):

    user_crazybones = req.user.profile.cb.all()

    search_method = req.GET['search_method']
    search_query = req.GET['search_query'].strip()

    radio_selected = False
    
    try: 
        error = req.GET['error']
    except:
        error = None

    if search_query == req.user.username and search_method == "user_name":
        form = TradeSearchForm(req.GET)
        return render(req, 'trades/form.html', {'form':form, 'error':"Big Time Error"})

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
    elif search_method == 'direct':
        try:
            user_id = req.GET['user_id']
            crazybone = Crazybone.objects.get(id=search_query)
            profile = Profile.objects.get(id=user_id)
            results = [{
                "user": profile.user.username,
                "cb": crazybone.name
            }]
            radio_selected = True
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

    return render(req, 'battle/results.html', {'results': results, 'user_crazybones':user_crazybones, 'search_method':search_method, 'radio_selected': radio_selected, 'error':error})

@login_required
def create(req):
    selected_values = req.POST['selected'].split('-')

    if req.user.username == selected_values[0]:
        return redirect(req.META['HTTP_REFERER']+"&error=tradewithself")

    try:
        new_user_from = req.user.profile
        new_user_to = User.objects.get(username__iexact=selected_values[0]).profile
        new_cb_offered = new_user_from.cb.get(name__iexact=req.POST['offered'])
        new_cb_wanted = new_user_to.cb.get(name__iexact=selected_values[1])
        new_trade = TradeRequest.objects.create(user_from=new_user_from, user_to=new_user_to, cb_wanted=new_cb_wanted, cb_offered=new_cb_offered)
        return redirect('trade-user')
    except Exception as err:
        print(err)
        return redirect(req.META['HTTP_REFERER']+"&error=true")

@login_required
def user(req):
    try:
        trades_made = TradeRequest.objects.filter(user_from=req.user.profile).order_by('-date').order_by('status')
        trades_received = TradeRequest.objects.filter(user_to=req.user.profile).order_by('-date').order_by('status')
    except:
        trades_made = None
        trades_received = None
    return render(req, 'trades/user.html', {'trades_made':trades_made, 'trades_received':trades_received, 'error': None})

@login_required
def action(req, trade_id):
    trade = TradeRequest.objects.get(id=trade_id)
    user_to = trade.user_to

    if req.user.username != user_to.user.username:
        print("hi")
        return redirect('trade-user')
    elif trade.status != "P":
        print("hi2")
        return redirect('trade-user')

    if req.POST['accept_trade'] == "Yes":
        # #Crazybone Trading
        user_from = trade.user_from
        cb_wanted = trade.cb_wanted
        cb_offered = trade.cb_offered

        user_from.cb.add(cb_wanted)
        user_from.cb.remove(cb_offered)

        user_to.cb.add(cb_offered)
        user_to.cb.remove(cb_wanted)

        trade.status = "A"
        trade.save()
        print(trade.status)

        # Trade Request PURGE
        # User_from
        user_from_trades = TradeRequest.objects.filter(user_to=user_from, cb_wanted=cb_offered, status="P").union(TradeRequest.objects.filter(user_from=user_from, cb_offered=cb_offered, status="P"))
        for trade in user_from_trades:
            trade.status = "R"
            trade.save()

        # User_to
        user_to_trades = TradeRequest.objects.filter(user_to=user_to, cb_wanted=cb_wanted, status="P").union(TradeRequest.objects.filter(user_from=user_to, cb_offered=cb_wanted, status="P"))
        for trade in user_to_trades:
            trade.status = "R"
            trade.save()
        
    elif req.POST['accept_trade'] == "No":
        trade.status = "R"
        trade.save()
    else:
        pass
    
    return redirect('trade-user')