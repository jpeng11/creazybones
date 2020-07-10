from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from main_app.models import Crazybone, TradeRequest, Profile, Cb_Profile, Battle, Notification
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
        def_battles = Battle.objects.filter(challenger=req.user.profile, challenger_cb=cbP.cb).count()
        cha_battles = Battle.objects.filter(defender=req.user.profile, defender_cb=cbP.cb).count()
        battle_num = def_battles + cha_battles
        print(battle_num)
        for x in range(0, cbP.qty):
            if x<battle_num:
                if cbP.qty == 1:
                    user_crazybones.append({
                        "value": cbP.cb.name,
                        "name": f"{cbP.cb.name} is in a battle"
                    })
                else:
                    user_crazybones.append({
                        "value": cbP.cb.name,
                        "name": f"{cbP.cb.name} ({x+1}) is in a battle"
                    })
            elif cbP.qty == 1:
                user_crazybones.append({
                    "value": cbP.cb.name,
                    "name": f"{cbP.cb.name}"
                })
            else:
                user_crazybones.append({
                    "value": cbP.cb.name,
                    "name": f"{cbP.cb.name} ({x+1})"
                })

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
                    def_battles = Battle.objects.filter(challenger=cbP.profile, challenger_cb=cbP.cb).count()
                    cha_battles = Battle.objects.filter(defender=cbP.profile, defender_cb=cbP.cb).count()
                    battle_num = def_battles + cha_battles
                    for x in range(0, cbP.qty):
                        if x<battle_num:
                            if cbP.qty == 1:
                                results.append({
                                    "user": cbP.profile.user.username,
                                    "cb": crazybone.name,
                                    "battle": True
                                })
                            else:
                                results.append({
                                    "user": cbP.profile.user.username,
                                    "cb": crazybone.name,
                                    "num": f"{x+1}",
                                    "battle": True
                                })
                        elif cbP.qty == 1:
                            results.append({
                                "user": cbP.profile.user.username,
                                "cb": crazybone.name,
                                "battle": False
                            })
                        else:
                            results.append({
                                "user": cbP.profile.user.username,
                                "cb": crazybone.name,
                                "num": f"{x+1}",
                                "battle": False
                            })
            else:
                results = "No user has that Crazy Bone yet."
        except Exception as err:
            results = None
    elif search_method == 'direct':
        try:
            user_id = req.GET['user_id']
            crazybone = Crazybone.objects.get(id=search_query)
            profile = Profile.objects.get(id=user_id)
            cbP = Cb_Profile.objects.get(profile=profile, cb=crazybone)
            def_battles = Battle.objects.filter(challenger=cbP.profile, challenger_cb = cbP.cb).count()
            cha_battles = Battle.objects.filter(defender=cbP.profile, defender_cb = cbP.cb).count()
            battle_num = def_battles + cha_battles
            results = []
            for x in range(0, cbP.qty):
                if x<battle_num:
                    if cbP.qty == 1:
                        results.append({
                            "user": profile.user.username,
                            "cb": crazybone.name,
                            "battle": True
                        })
                    else:
                        results.append({
                            "user": profile.user.username,
                            "cb": crazybone.name,
                            "num": f"{x+1}",
                            "battle": False
                        })
                elif cbP.qty == 1:
                    results.append({
                        "user": profile.user.username,
                        "cb": crazybone.name,
                        "battle": False
                    })
                else:
                    results.append({
                        "user": profile.user.username,
                        "cb": crazybone.name,
                        "num": f"{x+1}",
                        "battle": False
                    })
            radio_selected = True
        except Exception as err:
            print(err)
            results = None
    else:
        try:
            user = User.objects.get(username__iexact=search_query)
            crazybones = User.objects.get(username__iexact=search_query).profile.cb.all()
            results = []
            for cbP in Cb_Profile.objects.filter(profile=user.profile):
                def_battles = Battle.objects.filter(challenger=cbP.profile, challenger_cb = cbP.cb).count()
                cha_battles = Battle.objects.filter(defender=cbP.profile, defender_cb = cbP.cb).count()
                battle_num = def_battles + cha_battles
                for x in range(0, cbP.qty):
                    if x<battle_num:
                        if cbP.qty == 1:
                            results.append({
                                "user": search_query,
                                "cb": cbP.cb.name,
                                "battle": True
                            })
                        else:
                            results.append({
                                "user": search_query,
                                "cb": cbP.cb.name,
                                "num": f"{x+1}",
                                "battle": True
                            })
                    elif cbP.qty == 1:
                        results.append({
                            "user": search_query,
                            "cb": cbP.cb.name,
                            "battle": False
                        })
                    else:
                        results.append({
                            "user": search_query,
                            "cb": cbP.cb.name,
                            "num": f"{x+1}",
                            "battle": False
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
        new_notif = Notification.objects.create(notification_type="T", noti_from=new_user_from, noti_to=new_user_to)
        new_trade = TradeRequest.objects.create(user_from=new_user_from, user_to=new_user_to, cb_wanted=new_cb_wanted, cb_offered=new_cb_offered, created_notification=new_notif)
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
        print("YES")

        # Crazybone Trading variables defined, user_to is defined above because we need to use it earlier
        trade_user_from = trade.user_from
        trade_cb_wanted = trade.cb_wanted
        trade_cb_offered = trade.cb_offered

        trade.status = "A"
        trade.save()
        trade.created_notification.delete()

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

                # Purge trades since this cb is no longer available
                # Removing received trades for User_from
                user_from_received_trades = TradeRequest.objects.filter(user_to=trade_user_from, cb_wanted=trade_cb_offered, status="P")
                for trade_r in user_from_received_trades:
                    trade_r.status = "R"
                    trade_r.save()
                    trade_r.created_notification.delete()
                # Removing sent trades for User_from
                user_from_sent_trades = (TradeRequest.objects.filter(user_from=trade_user_from, cb_offered=trade_cb_offered, status="P"))
                for trade_s in user_from_sent_trades:
                    trade_s.status = "R"
                    trade_s.save()
                    trade_s.created_notification.delete()

            else:
                cbP_user_from.qty -= 1
                cbP_user_from.save()

                # Removing user_from trades IF all their crazy bones are battling
                def_battles = Battle.objects.filter(challenger=trade_user_from, challenger_cb=trade_cb_offered).count()
                cha_battles = Battle.objects.filter(defender=trade_user_from, defender_cb=trade_cb_offered).count()
                battle_num = def_battles + cha_battles

                if battle_num >= cbP_user_from.qty:
                    # Removing received trades for User_from
                    user_from_received_trades = TradeRequest.objects.filter(user_to=trade_user_from, cb_wanted=trade_cb_offered, status="P")
                    for trade_r in user_from_received_trades:
                        trade_r.status = "R"
                        trade_r.save()
                        trade_r.created_notification.delete()
                    # Removing sent trades for User_from
                    user_from_sent_trades = (TradeRequest.objects.filter(user_from=trade_user_from, cb_offered=trade_cb_offered, status="P"))
                    for trade_s in user_from_sent_trades:
                        trade_s.status = "R"
                        trade_s.save()
                        trade_s.created_notification.delete()

            #Remove cb_wanted or reduce qty for user_to
            if cbP_user_to.qty == 1:
                trade_user_to.cb.remove(trade_cb_wanted)

                # Purge trades since this cb is no longer available
                # Removing received trades for User_to
                user_to_received_trades = TradeRequest.objects.filter(user_to=trade_user_to, cb_wanted=trade_cb_wanted, status="P")
                for trade_r in user_to_received_trades:
                    trade_r.status = "R"
                    trade_r.save()
                    trade_r.created_notification.delete()
                # Removing sent trades for User_to
                user_to_sent_trades = (TradeRequest.objects.filter(user_from=trade_user_to, cb_offered=trade_cb_wanted, status="P"))
                for trade_s in user_to_sent_trades:
                    trade_s.status = "R"
                    trade_s.save()
                    trade_s.created_notification.delete()
            
            else:
                cbP_user_to.qty -= 1
                cbP_user_to.save()

                # Removing user_to trades IF all their crazy bones are battling
                def_battles = Battle.objects.filter(challenger=trade_user_to, challenger_cb=trade_cb_wanted).count()
                cha_battles = Battle.objects.filter(defender=trade_user_to, defender_cb=trade_cb_wanted).count()
                battle_num = def_battles + cha_battles
                if battle_num >= cbP_user_to.qty:
                    # Removing received trades for User_to
                    user_to_received_trades = TradeRequest.objects.filter(user_to=trade_user_to, cb_wanted=trade_cb_wanted, status="P")
                    for trade_r in user_to_received_trades:
                        trade_r.status = "R"
                        trade_r.save()
                        trade_r.created_notification.delete()
                    # Removing sent trades for User_to
                    user_to_sent_trades = (TradeRequest.objects.filter(user_from=trade_user_to, cb_offered=trade_cb_wanted, status="P"))
                    for trade_s in user_to_sent_trades:
                        trade_s.status = "R"
                        trade_s.save()
                        trade_s.created_notification.delete()

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
        
    elif req.POST['accept_trade'] == "No":
        trade.status = "R"
        trade.created_notification.delete()
        trade.save()
    else:
        pass
    
    return redirect('trade-user')