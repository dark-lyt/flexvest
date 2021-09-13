from django.utils.encoding import force_text
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from account.tokens import AccountActivationTokenGenerator
from datetime import timedelta
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.http.response import HttpResponse
from account.forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from account.models import Profile
from core.models import Plan, PlanGrowth, Referral, SelectPlan, Withdraw
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from flexvest.settings import EMAIL_HOST_USER as admin_mail
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.views import View


def register(request, **kwargs):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():

            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the user object

            # DE-ACTIVATE THE USER ON SIGNUP
            new_user.is_active = False
            new_user.save()

            country = user_form.cleaned_data['country']
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            phone_number = user_form.cleaned_data['phone_number']
            select_plan = user_form.cleaned_data['select_plan']
            gender = user_form.cleaned_data['gender']
            createSelectedPlan(select_plan, new_user)
            print(new_user.email)

            Profile.objects.create(user=new_user, country=country, phone_number=phone_number, gender=gender)
            if profile_id is not None:
                person = Profile.objects.get(id=profile_id)
                prof = Profile.objects.get(user=new_user)
                prof.recomended_by = person.user
                Referral.objects.create(user=person.user)
                prof.save()

            #  Sending authentication/otp to user
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template()
            # and calls its render() method immediately.
            message = render_to_string('account/activation_request.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(new_user),
            })
            send_mail(subject=subject, message=message, from_email=admin_mail,
                      recipient_list=[new_user.email], fail_silently=False)
            return redirect('account:activation_sent')
        # else:
        #     return render(request, 'account/registers.html', {'form': user_form, 'error': user_form.errors})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registers.html', {'form': user_form})


# def activate(request, uidb64, token):
#     user = User.objects.get(pk=uid)
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     # checking if the user exists, if the token is valid.
#     if user is not None and AccountActivationTokenGenerator.check_token(user=user, token=token):
#         # if valid set active true
#         user.is_active = True
#         # set signup_confirmation true
#         # user.profile.signup_confirmation = True
#         user.profile.signup_confirmation = True
#         user.save()
#         user.save()

#         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return redirect('core:dashboard')
#     else:
#         return render(request, 'activation_invalid.html')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.profile.signup_confirmation = True
            user.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            login(request, user)
            return redirect('core:dashboard')
        else:
            # invalid link
            return render(request, 'activation_invalid.html')


def activation_sent(request):
    return render(request, "account/activation-sent.html")


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    request.session.set_expiry(10)  # if remember me is
                    request.session.modified = True
                    login(request, user)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error while updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/editProfile.html', {'user_form': user_form, 'profile_form': profile_form})


# UTILS
def createSelectedPlan(plan, user):
    plan = plan[0]
    SelectPlan.objects.create(plan=plan, user=user)
    PlanGrowth.objects.create(plan=plan, user=user)
    Withdraw.objects.create(user=user)


# GET THE USER WHO HAS THE LINK AND REDIRECT TO NEW USER REG
def getRecProfile(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    if code:
        try:
            profile = Profile.objects.get(ref_code=code)
            request.session['ref_profile'] = profile.id
            print('id', profile.id)
        except Exception as e:
            print(e)
            print("Code doesn't exixt")
    return redirect("account:signup")


def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    plan = SelectPlan.objects.get(user=request.user).plan
    link = profile.getLink()
    current_site = get_current_site(request)
    current_site = current_site.domain
    return render(request, "account/myProfile.html", {'profile': profile, 'link': current_site + link, 'plan': plan})
