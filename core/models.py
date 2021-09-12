from account.models import Profile
from django.db.models.fields import DateTimeField
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from cryptocurrency_payment.models import CryptoCurrencyPayment
from django.utils import timezone


LABEL_CHOICES = (
    ('DS', 'A Starter Pack'),
    ('DP', 'Professional Pack'),
    ('DPR', 'Premium Pack'),
)


class Plan(models.Model):
    title = models.CharField(max_length=100)
    label = models.CharField(choices=LABEL_CHOICES, max_length=3)
    max_price = models.FloatField()
    min_price = models.FloatField()
    slug = models.SlugField()
    rate = models.FloatField()
    description1 = models.CharField(max_length=30)
    description2 = models.CharField(max_length=30)
    description3 = models.CharField(max_length=30)
    description4 = models.CharField(max_length=30)
    description5 = models.CharField(max_length=30)
    description6 = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})


class SelectPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    payed = models.BooleanField(default=False)
    pay_amt = models.FloatField(default=0.0)
    def __str__(self):
        return f'{self.user} on {self.plan.title} plan'




class Withdraw(models.Model):
    sent = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    is_able = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.user}"


class PlanGrowth(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    last_gained_date = DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} on {self.plan}'


class Referral(models.Model):
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.invitee}'

