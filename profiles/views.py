from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from profiles.models import UserClass
from applications.models import Notification
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from homepage import email_vendor

# logout functionality
@login_required
def logout_function(request):

    if request.user.user_type == 'ADM':
        url_redirect = '/admin'
    else:
        url_redirect = '/'

    logout(request)

    return redirect(url_redirect)

def signup_function(request):
    """Create new user account based on provided credentials"""
    if request.method == 'POST':
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        last_name = request.POST.get("last_name", "")
        first_name = request.POST.get("first_name", "")
        type = request.POST.get("type", "")
        new_user = UserClass.objects.create_basic_user(email=email, password=password, last_name=last_name,
                                                    first_name=first_name, type=type)
        new_user.save()

        # create new notification
        notification = Notification.objects.get_or_create(notification_type='C', is_dismissed=False, \
                                        basic_user=new_user)[0]
        notification.save()

        # sending emails to admin and new user
        email_vendor.email_admin_new_signup(new_user)
        email_vendor.email_user_new_signup(new_user)

        #logs in user after signing up
        user = authenticate(email=email, password=password)
        # check if user was retrieved from the database
        if user:
            # if user is active
            if user.is_active:
                # do login
                login(request, user)
                # return response for index page
                return redirect('/')
            else:
                # return response that account is inactive
                return HttpResponse("Account is inactive")
        else:
            print("login failed")
            return HttpResponse("Invalid login details given")
    else:
        # redirect user to login page
        return render(request, 'profiles/login.html', {})


def login_function(request):
    """Login user based on provided credentials"""
    # if request type is POST
    if request.method == 'POST':
        # get credentials
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        # check if user was retrieved from the database
        if user:
            # if user is active
            if user.is_active:
                # do login
                login(request, user)
                # return response for index page
                return redirect('/')
            else:
                # return response that account is inactive
                return HttpResponse("Account is inactive")
        else:
            print("login failed")
            return redirect("/login")
    else:
        # redirect user to login page
        return render(request, 'profiles/login.html', {})
