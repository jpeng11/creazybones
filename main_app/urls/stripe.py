from django.urls import path
from ..views import stripe

urlpatterns = [
    path('config/', stripe.stripe_config, name='stripe'),
    path('create-checkout-session/', stripe.create_checkout_session),
    path('success/', stripe.success),
    path('cancelled/', stripe.CancelledView.as_view()),
]
