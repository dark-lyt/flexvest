from datetime import timedelta
from django.contrib import messages
from django.http.response import HttpResponse
from account.forms import LoginForm, ProfileEditForm, UserEditForm, UserRegistrationForm
from account.models import Profile
from core.models import Plan, PlanGrowth, SelectPlan
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
get_object_or_404
# Create your views here.


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
            new_user.save()
            
            country = user_form.cleaned_data['country']
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            phone_number = user_form.cleaned_data['phone_number']
            select_plan = user_form.cleaned_data['select_plan']
            gender = user_form.cleaned_data['gender']
            print(select_plan)
            createSelectedPlan(select_plan, new_user)
           
            Profile.objects.create(user=new_user, country=country, phone_number=phone_number, gender=gender)
            if profile_id is not None:
                person = Profile.objects.get(id=profile_id)
                prof = Profile.objects.get(user=new_user)
                prof.recomended_by = person.user
                prof.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("core:home")
        else:
            return render(request, 'account/registers.html', {'form': user_form, 'error': user_form.errors})
            
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registers.html',{'form': user_form})


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
    plan =plan[0]
    SelectPlan.objects.create(plan=plan, user=user)
    PlanGrowth.objects.create(plan=plan, user=user)


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
    return render(request, "account/myProfile.html", {'profile': profile, 'link': current_site + link, 'plan':plan})
        
