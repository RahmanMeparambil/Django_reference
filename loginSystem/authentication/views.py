from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'authentication/home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username=username,email=email,password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname 
        myuser.save()
        
        messages.success(request,"Account created successfully!")
        return redirect('home')
    return render(request,'authentication/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username,password=password)
        if user :
            login(request,user)
            messages.success(request,"Login successful")
            return render(request,'authentication/home.html',{'fname':user.first_name})
        else :
            messages.error(request,"Bad credentials")
            return redirect('home')
    return render(request,'authentication/signin.html')


def signout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('home')