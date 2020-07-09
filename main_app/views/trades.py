from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main_app.models import Crazybone, TradeRequest, Profile, Cb_Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from main_app.forms import TradeSearchForm


@login_required
def index(req):
    return render(req, 'trades/form.html', {'form':TradeSearchForm, 'error':None})

@login_required
def result(req):

    user_crazybones = []

    for cbP in Cb_Profile.objects.filter(profile=req.user.profile):
        for x in range(0, cbP.qty):
            user_crazybones.append(cbP.cb.name)


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
            cbPs = Cb_Profile.objects.filter(cb=crazybone)
            if(len(cbPs) != 0):
                results = []
                for cbP in cbPs:
                    for x in range(0, cbP.qty):
                        results.append({
                            "user": cbP.profile.user.username,
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
            for cbP in Cb_Profile.objects.filter(profile=user.profile):
                for x in range(0, cbP.qty):
                    results.append({
                        "user": search_query,
                        "cb": cbP.cb.name
                    })
        except:
            results = None

    return render(req, 'trades/results.html', {'results': results, 'user_crazybones':user_crazybones, 'search_method':search_method, 'radio_selected': radio_selected, 'error':error})

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
        trades_made = TradeRequest.objects.filter(user_from=req.user.profile).order_by('-date')
        trades_received = TradeRequest.objects.filter(user_to=req.user.profile).order_by('-date')
    except:
        trades_made = None
        trades_received = None
    return render(req, 'trades/user.html', {'trades_made':trades_made, 'trades_received':trades_received, 'error': None})

@login_required
def action(req, trade_id):

    # Check if this is a valid trade-id, if not send it back to the trades-page for the user
    try:
        trade = TradeRequest.objects.get(id=trade_id)
        trade_user_to = trade.user_to
    except:
        return redirect('trade-user')

    # Check if this trade actually belongs to the user that's accepting/logged in and that the trade is still pending.
    if req.user.username != trade_user_to.user.username:
        return redirect('trade-user')
    elif trade.status != "P":
        return redirect('trade-user')

    # Once all the checks are done, we can start proceeding with the trade
    if req.POST['accept_trade'] == "Yes":
        # Crazybone Trading variables defined, user_to is defined above because we need to use it earlier
        trade_user_from = trade.user_from
        trade_cb_wanted = trade.cb_wanted
        trade_cb_offered = trade.cb_offered

        # The user sending the request will lose the cb they offered, and the user receiving the request will lose the cb that is being requested.
        # First check if the relationship between cb and profile exist (At this point it should). If for some reason it doesn't we redirect and do nothing.
        # If it exist and qty = 1, remove cb, if it is higher, we just subtract 1 from the qty.
        try: 
            # Check the relationship for both users right away before we do anything
            cbP_user_from = Cb_Profile.objects.get(cb=trade_cb_offered, profile=trade_user_from)
            cbP_user_to = Cb_Profile.objects.get(cb=trade_cb_wanted, profile=trade_user_to)

            #Remove cb_offered or reduce qty for user_from
            if cbP_user_from.qty == 1:
                trade_user_from.cb.remove(trade_cb_offered)
            else:
                cbP_user_from.qty -= 1
                cbP_user_from.save()

            #Remove cb_wanted or reduce qty for user_to
            if cbP_user_to.qty == 1:
                trade_user_to.cb.remove(trade_cb_wanted)
            else:
                cbP_user_to.qty -= 1
                cbP_user_to.save()

        except:
            return redirect('trade-user')

        # The user sending request will have the cb_wanted added - First check if it already exist, if not, add the cb
        try: 
            cbP = Cb_Profile.objects.get(cb=trade_cb_wanted, profile=trade_user_from)
            cbP.qty += 1
            cbP.save()
        except:
            trade_user_from.cb.add(trade_cb_wanted)

        # The user receiving request will have the cb_offered added - First check if it already exist, if not, add the cb
        try: 
            cbP = Cb_Profile.objects.get(cb=trade_cb_offered, profile=trade_user_to)
            cbP.qty += 1
            cbP.save()
        except:
            trade_user_to.cb.add(trade_cb_offered)

        trade.status = "A"
        trade.save()
        print(trade.status)

        # Trade Request PURGE - An accepted trade may render other trades impossible as a person may trade away a crazybone crucial to that trade.
        # Therefore, we need to remove any trades that are now impossible due to the accepted trade.

        # Removing received trades for User_from
        user_from_received_trades = TradeRequest.objects.filter(user_to=trade_user_from, cb_wanted=trade_cb_offered, status="P")
        for trade in user_from_received_trades:
            if trade.cb_wanted not in trade_user_from.cb.all():
                trade.status = "R"
                trade.save()

        # Removing sent trades for User_from
        user_from_sent_trades = (TradeRequest.objects.filter(user_from=trade_user_from, cb_offered=trade_cb_offered, status="P"))
        for trade in user_from_sent_trades:
            if trade.cb_offered not in trade_user_from.cb.all():
                trade.status = "R"
                trade.save()

        # Removing received trades for User_to
        user_to_received_trades = TradeRequest.objects.filter(user_to=trade_user_to, cb_wanted=trade_cb_wanted, status="P")
        for trade in user_to_received_trades:
            if trade.cb_wanted not in trade_user_to.cb.all():
                trade.status = "R"
                trade.save()

        # Removing sent trades for User_to
        user_to_sent_trades = (TradeRequest.objects.filter(user_from=trade_user_to, cb_offered=trade_cb_wanted, status="P"))
        for trade in user_to_sent_trades:
            if trade.cb_offered not in trade_user_to.cb.all():
                trade.status = "R"
                trade.save()
        
    elif req.POST['accept_trade'] == "No":
        trade.status = "R"
        trade.save()
    else:
        pass
    
    return redirect('trade-user')