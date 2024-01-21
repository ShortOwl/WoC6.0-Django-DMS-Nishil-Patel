from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm


#Importing for creating a login page

from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileInfoForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) #setting up the hash.
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user #re-establishing the one - to - one relationship defined in UserProfileInfoForm

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

                
                
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{'user_form' : user_form,'profile_form' : profile_form,'registered' : registered})



#Creating the login view
def log_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #using Django's builtin authenticate function
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else :
                return HttpResponse('Sorry,your account is not active!')
        else :
            print('Anonymous login request and it failed.')
            print(f'Username : {username} and Password : {password}')
            return HttpResponse('Invalid Login Details')
    else:
        return render(request,'basic_app/login.html')
            

#Using Decorators to Logout of after logging in 
@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def special(request):
    return HttpResponse('You are logged in!')
    

