from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Purchase
from .forms import PurchaseForm

import stripe


def upgrade(request):
    """ A review to return the pro page. """
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return redirect('account_login')
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "GET":
        if user.userprofile.pro_user:
            messages.info(request, "You already have a Pro account! You rock!")
            profile = user.userprofile
            context = {
                "profile": profile,
            }
            return redirect('dashboard', context)
        else:
            cost = settings.PRO_LIFETIME_CHARGE
            form = PurchaseForm(initial={"purchase_amount": cost})
            stripe_cost = round(cost * 100)
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_cost,
                currency=settings.STRIPE_CURRENCY,
            )

            if not stripe_public_key:
                messages.warning(request, "Stripe public key is missing.")

            context = {
                "stripe_public_key": stripe_public_key,
                "client_secret": intent.client_secret,
                "form": form,
                "user": user,
                "cost": cost,
            }
            return render(request, "pro/upgrade.html", context)
    else:
        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "country": request.POST["country"],
            "user": request.user,
            "purchase_amount": request.POST.get("purchase_amount", settings.PRO_LIFETIME_CHARGE)
        }
        print(request.POST.get("purchase_amount"))
        purchase_form = PurchaseForm(form_data)
        if purchase_form.is_valid():
            purchase = purchase_form.save(commit=False)
            pid = request.POST.get("client_secret").split("_secret")[0]
            purchase.stripe_pid = pid
            purchase.save()
            print("Success!")
            return redirect(reverse("upgrade_success", args=[purchase.order_number]))
        else:
            messages.error(request, "Purchase failed. Please recheck your information.")


def upgrade_success(request, order_number):
    """ A view to handle successful upgrade purchase """
    if request.user.is_authenticated:
        purchase = get_object_or_404(Purchase, order_number=order_number)
        messages.success(request,
                         f"Purchase successful! Your order number is {purchase.order_number}. A confirmation email will be sent to {purchase.email}")
        context = {
            "purchase": purchase,
        }
        user = User.objects.get(username=purchase.user)
        user.userprofile.pro_user = True
        user.userprofile.save()
        user.save()
        return render(request, "pro/upgrade_success.html", context)


def benefits(request):
    """ A review to return the benefits page. """

    return render(request, "pro/benefits.html")
