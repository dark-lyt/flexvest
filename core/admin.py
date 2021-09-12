from django.contrib import admin

from .models import Plan, PlanGrowth, Referral, SelectPlan, Withdraw
# Register your models here.
admin.site.register(Plan)
admin.site.register(PlanGrowth)
admin.site.register(SelectPlan)
admin.site.register(Referral)
admin.site.register(Withdraw)