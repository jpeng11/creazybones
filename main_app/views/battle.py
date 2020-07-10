from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from ..models import Crazybone, Comment, Profile, Battle, Notification, Cb_Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from main_app.forms import BattleSearchForm

@login_required
def index(req):
    return render(req, 'battle/index.html', {'form': BattleSearchForm })

@login_required
def battle(req):
    pass

@login_required
def result(req):

    user_crazybones = req.user.profile.cb.all()
    if len(user_crazybones) <= 0:
        form = BattleSearchForm(req.GET)
        return render(req, 'battle/index.html', {'form': form, 'error': 'You have no crazybones to battle with'})

    search_method = req.GET['search_method']
    search_query = req.GET['search_query'].strip()

    radio_selected = False
    
    try: 
        error = req.GET['error']
    except:
        error = None

    if search_query == req.user.username and search_method == "user_name":
        form = BattleSearchForm(req.GET)
        print('HEEEEEEEERE')
        return render(req, 'battle/index.html', {'form':form, 'error':"Big Time Error"})

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
    #create notification

    def_cb = req.POST['defender-cb'].split('-')
    defender = User.objects.get(username__iregex=f'^{def_cb[0]}$').profile
    defender_cb = Crazybone.objects.get(name=def_cb[1])
    challenger_cb = Crazybone.objects.get(name=req.POST['challenger_cb'])
    battle_noti = Notification.objects.create(notification_type='B', noti_from=req.user.profile, noti_to=defender)
    battle = Battle.objects.create(challenger=req.user.profile, defender=defender, challenger_cb=challenger_cb, defender_cb=defender_cb, turn='D', created_notification = battle_noti)
    return redirect('battle_display', battle_id = battle.id)

@login_required
def notification(req, notif_id):
    this_noti = Notification.objects.get(id = notif_id)
    if(this_noti.noti_to == req.user.profile):    
        this_battle = Battle.objects.get(created_notification = this_noti)
        return redirect('battle_display', battle_id = this_battle.id)
    else:
        return redirect('')

@login_required
def display(req, battle_id):
    #if winner != N & Notification belongs to req.user.profile, delete the notification
    battle = Battle.objects.get(id=battle_id)
    this_noti = battle.created_notification
    print(req.user.profile.id, battle.challenger.id, battle.defender.id)
    if req.user.profile.id == battle.challenger.id or req.user.profile.id == battle.defender.id:
        if not battle.accepted:
            return render(req, 'battle/pending.html', {'battle': battle})
        if battle.winner != 'N':
            if this_noti.noti_to == req.user.profile:
                this_noti.delete()
            winner = battle.challenger if battle.winner == 'C' else battle.defender
            return render(req, 'battle/finished.html', {'battle': battle, 'winner': winner})
        if battle.turn == 'C':
            turn = {
                'id': battle.challenger.id,
                'name': battle.challenger,
                'cb': battle.challenger_cb
            }
            other = {
                'id': battle.defender.id,
                'name': battle.defender,
                'cb': battle.defender_cb
            }
        else:
            turn = {
                'id': battle.defender.id,
                'name': battle.defender,
                'cb': battle.defender_cb
            }
            other = {
                'id': battle.challenger.id,
                'name': battle.challenger,
                'cb': battle.challenger_cb
            }
        return render(req, 'battle/display.html', {'battle': battle, 'turn': turn, 'other': other})
    else:
        return redirect('battle_error', battle_id=battle.id)
    
    

@login_required
def accept(req, pk, noti_type):
    sent_from = Profile.objects.get(user__id = pk)
    this_noti = Notification.objects.filter(noti_to = req.user.profile)
    this_noti = this_noti.filter(noti_from = sent_from)
    this_noti = this_noti.get(notification_type = noti_type)
    battle = Battle.objects.get(created_notification=this_noti)
    this_noti.notification_type = 'M'
    this_noti.save()
    #change from B to M
    if battle.accepted == False or req.user.profile.id == battle.defender.id or req.user.profile.id == battle.challenger.id:
        battle.accepted = True
        battle.save()
        return redirect('battle_display', battle_id=battle.id)
    else:
        return redirect('battle_error', battle_id=battle.id)

@login_required
def reject(req, pk, noti_type):
    sent_from = Profile.objects.get(user__id = pk)
    this_noti = Notification.objects.filter(noti_to = req.user.profile)
    this_noti = this_noti.filter(noti_from = sent_from)
    this_noti = this_noti.get(notification_type = noti_type)
    battle = Battle.objects.get(created_notification=this_noti)
    battle.delete()
    this_noti.delete()
    return redirect('notifications')

@login_required
def error(req, battle_id):
    battle = Battle.objects.get(id=battle_id)
    return render(req, 'battle/rejected.html', {'battle': battle})

def move(req, battle_id):
    # delete notification
    move = req.POST['move']
    battle = Battle.objects.get(id=battle_id)
    last_turn = battle.turn
    this_noti = battle.created_notification
    # this_noti.delete()
    if move == 'hit':
        battle.winner = last_turn
        battle.save()

        if last_turn == 'C':
            # Challenger wins the CB of defender - Check if the relationship exist first, if it does, add to qty, otherwise add CB directly.
            try:
                cbP_adding = Cb_Profile.objects.get(profile=battle.challenger, cb=battle.defender_cb)
                cbP_adding.qty += 1
                cbP_adding.save()
            except:
                battle.challenger.cb.add(battle.defender_cb)

            # Defender loses their CB. If the quantiy is higher than 1, just subtract 1, otherwise remove the CB from the defender.
            cb_removing = Cb_Profile.objects.get(profile=battle.defender, cb=battle.defender_cb)
            if cb_removing.qty > 1:
                cb_removing.qty -= 1
                cb_removing.save()
            else:
                cb_removing.delete()

            this.noti_from = battle.challenger
            this_noti.noti_to = battle.defender
            this_noti.save()   
        else:
            # Defender wins the CB of the challenger - Check if the relationship exist first, if it does, add to qty, otherwise add CB directly.
            try:
                cbP_adding = Cb_Profile.objects.get(profile=battle.defender, cb=battle.challenger_cb)
                cbP_adding.qty += 1
                cbP_adding.save()
            except:
                battle.defender.cb.add(battle.challenger_cb)
            
            # Challenger loses their CB. If the quantiy is higher than 1, just subtract 1, otherwise remove the CB from the defender.
            cb_removing = Cb_Profile.objects.get(profile=battle.challenger, cb=battle.challenger_cb)
            if cb_removing.qty > 1:
                cb_removing.qty -= 1
                cb_removing.save()
            else:
                cb_removing.delete()
            
            this_noti.noti_from = battle.defender
            this_noti.noti_to = battle.challenger
            this_noti.save()

        return redirect('battle_display', battle_id=battle_id)
    elif move == 'miss':
        #create notification
        battle.turn = 'C' if battle.turn == 'D' else 'D'
        battle.save()
        temp = this_noti.noti_from
        this_noti.noti_from = this_noti.noti_to
        this_noti.noti_to = temp
        this_noti.save()
        return redirect('battle_display', battle_id=battle_id)
    return redirect('battle_error', battle_id=battle_id)
