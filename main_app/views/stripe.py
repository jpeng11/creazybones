import stripe
import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from ..models import Crazybone, Profile


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = os.environ['DOMAIN_URL']
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url +
                'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': '10 packs of Crazy Bone loot bags',
                        'quantity': 1,
                        'currency': 'cad',
                        'amount': '1000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def success(request):
    current_user = request.user.id
    cbs = []
    for z in range(10):
        rand_cb = Crazybone.objects.order_by('?')[0]
        cbs.append(rand_cb)
        request.user.profile.cb.add(rand_cb)
    return render(request, 'stripe/success.html', {'cbs': cbs})


class CancelledView(TemplateView):
    template_name = 'stripe/cancelled.html'
