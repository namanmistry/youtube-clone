from django.shortcuts import render,redirect
from .forms import RegisterUserForm
from django.http import HttpResponse
from .models import Account

USER_ID = 0

def get_user_id():
    return USER_ID

def register_user(request):
    if request.method == "POST":   
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("account created successfully")
    else:
        form = RegisterUserForm()
    return render(request, 'account/register.html',{'form': form})

def login_user(request):
    global USER_ID
    if request.method == "POST":
        if Account.objects.filter(email=request.POST.get("email"),password=request.POST.get("password")).exists():
            USER_ID = Account.objects.get(email=request.POST.get("email"),password=request.POST.get("password"))
            return redirect('/videos/')
        return HttpResponse("Wrong email or password")
    return render(request, 'account/login.html')

def logout_user(request):
    global USER_ID
    USER_ID = 0
    return redirect('/videos/')