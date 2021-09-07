from django.db.models.fields import SlugField
import schedule
import time
from cryptocurrency_payment import tasks
from datetime import datetime 
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect, reverse
import random
from django.contrib.auth.decorators import login_required
import string
from .forms import ContactForm, PayForm, WithdrawForm
from .models import Plan, Referral, SelectPlan, Withdraw  
from cryptocurrency_payment.models import CryptoCurrencyPayment, create_new_payment
from django.conf import settings
from django.core.mail import message, send_mail
from .models import PlanGrowth
from account.models import Profile
from django.contrib.sites.shortcuts import get_current_site

ADMIN_MAIL = 'amoakbeall@fuwari.be'


def home(request):
    return render(request, "core/coin.html")



def product(request, slug):
    plan = get_object_or_404(Plan, slug=slug)
    selected_plan, created = SelectPlan.objects.get_or_create(user=request.user, plan=plan)
    form = PayForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            cd = form.cleaned_data
            price = cd['coin_amount']
            if price >= plan.min_price and price <= plan.max_price:
                selected_plan.pay_amt = price
                selected_plan.save()
                return redirect('core:add-to-cart', slug=slug)
            else:
                messages.error(request, "Please enter a value with the range")
        else:
           messages.warning(request, "Form not valid")

    return render(request, 'core/product.html', {'form': form, 'plan': plan})



@login_required
def fund_account(request):
    user = request.user
    selected_plan = SelectPlan.objects.get(user=user)
    plan = selected_plan.plan
    prev_paid = selected_plan.pay_amt
    # max_payable = plan.max_price
    # min_payable = plan.min_price
    form = PayForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            cd = form.cleaned_data
            price = cd['amount']
            if price >= plan.min_price and price <= plan.max_price:
                selected_plan.pay_amt += price
                selected_plan.save()
                return redirect('core:add-to-cart', slug=plan.slug)
            else:
                messages.error(request, "Please enter a value with the range")
        else:
           messages.warning(request, "Form not valid")

    return render(request, 'core/fund.html', {'form':form, 'plan':plan})


@login_required
def add_to_cart(request, slug):
    selected_plan = SelectPlan.objects.get(user=request.user)
    payment = create_new_payment(crypto='BITCOIN',  # Cryptocurrency from your backend settings
                                 fiat_amount=selected_plan.pay_amt,  # Amount of actual item in fiat
                                 fiat_currency='USD',  # Fiat currency used to convert to crypto amount
                                 payment_title= str(selected_plan.plan.title + " By "+request.user.username),  # Title associated with payment
                                 payment_description=str(selected_plan.plan.title + " By "+request.user.username),  # Description associated with payment
                                 # Generic linked object for this payment -> crypto_payments = GenericRelation(CryptoCurrencyPayment)
                                 related_object=None,
                                 user=request.user,  # User of this payment for non-anonymous payment
                                 parent_payment=None,  # Obvious
                                 address_index=None,  # Use a particular address index for this payment
                                 reuse_address=None)  # Used previously paid address for this payment
    pid = payment.id
    pg, created = PlanGrowth.objects.get_or_create(user=request.user, plan=selected_plan.plan)

    return redirect(f"/paydetails/payment/{pid}")


def about(request):
    return render(request, "core/abouts.html")

def faq(request):
    return render(request, "core/faq.html")


@login_required
def dashboard(request):
    total = 0
    total_usd = 0
    plan = get_object_or_404(SelectPlan, user=request.user)
    profit = PlanGrowth.objects.get(user=request.user)
    total_commission = Referral.objects.filter(user=request.user)
    if len(total_commission) > 0:
        total_commission = total_commission[0].get_total_commision()
    else:
        total_commission = 0
    plan_title = plan.plan
    history = CryptoCurrencyPayment.objects.filter(user=request.user).order_by('-created_at')
    for history in history:
        if history.status == 'paid':
            total += history.crypto_amount
            total_usd += history.fiat_amount    
    
    return render(request, 'core/dashboard.html', {'plan_title': plan_title, 'total_usd': total_usd,
     'history': history, 'profit':profit.amount, 'commission':total_commission})




@login_required
def withdraw(request):
    form = WithdrawForm(request.POST or None)
    return render(request, 'core/withdraw.html', {"form":form})


@login_required
def my_referrals(request):
    profile = Profile.objects.get(user=request.user)
    link = profile.getLink()
    current_site = get_current_site(request)
    current_site = current_site.domain
    num = profile.get_recommened_profiles()
    if isinstance(num, list):
        num = len(num)
    
    referral = Referral(user=request.user)
    commission = referral.get_total_commision()

    return render(request, 'core/referral.html', {'link':current_site + link, 'num':num, 'commission':commission, 'referral':referral })





