from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.shortcuts import reverse
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from .myutils import generate_ref_code
# Create your models here.

GENDER_CHOICES = (
    ('', "Others"),
    ('M', 'Male'),
    ('F', 'Female')
)




class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    country = CountryField(null=True)
    phone_number = PhoneNumberField(null=True)
    ref_code = models.CharField(max_length=15)
    recomended_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='ref_by')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1 )
    signup_confirmation = models.BooleanField(default=False)



    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        my_recs = []
        for profile in qs:
            try:
                if profile.recomended_by == self.user:
                    my_recs.append(profile)
            except Exception as e:
                pass
        return my_recs


    def getLink(self):
        return reverse("account:get_profile", kwargs={"ref_code": self.ref_code})


    def save(self, *args, **kwargs):
        if self.ref_code == "":
            ref_code =  generate_ref_code()
            self.ref_code = ref_code
        super().save(*args, **kwargs)
