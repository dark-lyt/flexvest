from account.models import Profile
from core.models import PlanGrowth, Referral, SelectPlan
from cryptocurrency_payment.models import CryptoCurrencyPayment
from cryptocurrency_payment import tasks
import time
import schedule
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def growPlan():
    total_paid = 0
    plan = SelectPlan.objects.all()
    for person_plan in plan:
        gp, created = PlanGrowth.objects.get_or_create(plan=person_plan.plan, user=person_plan.user)
        history = CryptoCurrencyPayment.objects.filter(status="paid")
        if history:
            for story in history:
                total_paid += story.fiat_amount
            person_plan.pay_amt = total_paid
            if person_plan.plan == "DIGI-STARTER":
                current_earned = total_paid * 0.1
                gp.amount += current_earned
                gp.last_gained_date = datetime.now()
                gp.save()
            elif person_plan.plan == "DIGI-PRO":
                current_earned = total_paid * 0.15
                gp.amount += current_earned
                gp.last_gained_date = datetime.now()
                gp.save()
            else:
                current_earned = total_paid * 0.25
                gp.amount += current_earned
                gp.last_gained_date = datetime.now()
                gp.save()


def getCommission():
    subscribers = SelectPlan.objects.all()
    for person in subscribers:
        user = person.user
        person_profile = Profile.objects.get(user=user)
        recs = person_profile.get_recommened_profiles()
        if recs != 0:
            for rec in recs:
                gp = PlanGrowth.objects.get(user=rec.user)
                referral = Referral.objects.filter(user=user, invitee=rec.user)
                for ref in referral:
                    ref.ammount += gp.ammount * 0.1
                    ref.save()


def test():
    tasks.cancel_unpaid_payment()


def test2():
    tasks.refresh_payment_prices()


def test3():
    tasks.update_payment_status()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(test, 'interval', minutes=4)
    scheduler.add_job(test2, 'interval', minutes=2)
    scheduler.add_job(test3, 'interval', minutes=6)
    scheduler.add_job(getCommission, 'interval', minutes=7)
    scheduler.add_job(growPlan, 'interval', minutes=4)

    scheduler.start()


# form = WithdrawForm(request.POST or None)
    # if form.is_valid():
    #     address = form.cleaned_data.get('address')
    #     amount = form.cleaned_data.get('amount')
    #     amount = int(amount)
    #     # if amount > 0 and amount<= total_usd:
    #     if amount > 0:
    #         subject = form.cleaned_data.get('subject')
    #         message = f"Message from:{request.user}:\n{request.user} wishes to withdraw {amount} worth of btc from thier investment to\
    #             the address: {address}"
    #         recipient = ADMIN_MAIL
    #         # send_mail(subject, message, EMAIL_HOST_USER, [recipient   ], fail_silently=False)
    #         send_mail("Withdrawal Request: COINPACE", f"Your request for {amount} worth of BTC from\
    #             your investment has been recieved and will be sent to the address:\
    #                  {address} as you have provided with in the next 24hrs.\
    #                 Thank you for investing with us.", EMAIL_HOST_USER, request.user.email, fail_silently=False)
    #         messages.info(request, "Your request has been recieved")
    #         withdraw = Withdraw.objects.create(user=request.user, amount=amount)
    #
    # withdraw.save()
    #         return redirect("core:home")
    #     else:
    #         messages.info(request, "You are not able to withdraw at the moment")
