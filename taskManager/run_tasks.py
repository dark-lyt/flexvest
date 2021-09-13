from account.models import Profile
from core.models import PlanGrowth, Referral, SelectPlan, Withdraw
from cryptocurrency_payment.models import CryptoCurrencyPayment
from cryptocurrency_payment import tasks
import time
import schedule
from datetime import datetime
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler


def growPlan():
    total_paid = 0
    plan = SelectPlan.objects.all()
    for person_plan in plan:
        gp = PlanGrowth.objects.get(user=person_plan.user)
        history = CryptoCurrencyPayment.objects.all()
        
        #LOOP THROUGH ALL THE CRYPTO PAYMENT TO GET THE USER
        if history:
            for story in history:
                if story.user == person_plan.user and story.status == "paid":
                    total_paid += story.fiat_amount
            
            
            # if total_paid > 0:
                # CHECK FOR THE USERS PLAN AND ADD THE PERSON INTEREST RATE THERE
            person_plan.pay_amt = total_paid
            if person_plan.plan == "DIGI-STARTER":
                current_earned = total_paid * 0.1
                gp.amount += current_earned
                gp.last_gained_date = timezone.now()
                gp.save()
            elif person_plan.plan == "DIGI-PRO":
                current_earned = total_paid * 0.15
                gp.amount += current_earned
                gp.last_gained_date = timezone.now()
                gp.save()
            else:
                current_earned = total_paid * 0.25
                gp.amount += current_earned
                gp.last_gained_date = timezone.now()
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
                try:
                    referral = Referral.objects.get(invitee=rec.user)
                    print(referral)
                    referral.amount += gp.amount * 0.1
                    referral.save()
                except Exception as e:
                    print("User has no referral")




def is_able():
    gp = PlanGrowth.objects.all()
    for g in gp:
        user = g.user
        person = Withdraw.objects.get(user=user)
        last_gain = g.last_gained_date
        delta = timezone.now() - last_gain
        days = delta.days
        if days >= 14:
            person.is_able = True

def updateProfit():
    people = Withdraw.objects.all()
    for person in people:
        if person.sent:
            user = person.user
            user_inquest = PlanGrowth.objects.get(user=user)
            user_inquest.amount -= person.amount
            user_inquest.save()

def test():
    tasks.cancel_unpaid_payment()


def test2():
    tasks.refresh_payment_prices()


def test3():
    tasks.update_payment_status()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(test, 'interval', minutes=40)
    scheduler.add_job(test2, 'interval', minutes=20)
    scheduler.add_job(test3, 'interval', minutes=60)
    # scheduler.add_job(getCommission, 'interval', minutes=3)
    # scheduler.add_job(growPlan, 'interval', minutes=2)
    # scheduler.add_job(updateProfit, 'interval', minutes=9)
    # scheduler.add_job(is_able, 'interval', minutes=5)

    scheduler.start()



