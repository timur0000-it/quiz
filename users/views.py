from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail

from .models import *
from .forms import *
# Create your views here.

def login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        return redirect('users:signin')
    return wrapper

def gmail(user,code):
    subject = 'Поздравляем с регистрацией'
    message = f'Привет , {user.username}! рады приветствовать на нашем сайте код {code} http://127.0.0.1:8000/verify_code/'
    to_email = user.email
    send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[to_email]
            )

def signup(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            teacher = form.cleaned_data.get('teacher')
            if teacher == True:
                user.is_active = False
                obj,raw_code = ActivationCode.create_for_user(user)
                user.save()
                gmail(user,raw_code)
                request.session['active_email'] = user.email
                return redirect('users:verify_code')
            else:
                login(request,user)
            return redirect('chatting:all_rooms')
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})

def signin(request):
    form = SignInForm()
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username','').strip()
            password = form.cleaned_data.get('password','').strip()
            print(username)
            print(password)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('chatting:all_rooms')
            else:
                print(user)
                messages.warning(request, 'Неверный логин или пароль')
                return render(request,'signin.html',{'form':form})
    else:
        return render(request,'signin.html',{'form':form})



def verify_code(request):
    if request.method == 'POST':
        form = ActivationCodeForms(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code','')
            email = request.session['active_email']
            user1 = CustomerUser.objects.filter(email=email).order_by('-date_joined').first()
            user_code = ActivationCode.objects.filter(user=user1).order_by('-created_at').first()
            if not user_code:
                user1.delete()
                messages.warning(request, 'Вы не подтвердили код пожайлуста зарегестрируйтесь заново')
                return redirect('users:signin')  
            activation = user_code.check_code(code)
            if activation[0] == True:
                user1.is_active=True
                user1.save()
                login(request,user1)
                messages.success(request, 'Поздравляем с регистрацией')
                return redirect('chatting:all_rooms')
            else:
                form = ActivationCodeForms()
                email = request.session['active_email']
                form.fields['email'].initial=email
                error=activation[1]
                return render(request,'verify_code.html',{'form':form,'error':error})
    else:
        form = ActivationCodeForms()
        email = request.session['active_email']
        form.fields['email'].initial=email
    return render(request,'verify_code.html',{'form':form})


def re_send_code(request):
    email = request.session['active_email']
    user1 = CustomerUser.objects.filter(email=email).order_by('-date_joined').first()
    user_code = ActivationCode.objects.filter(user=user1).order_by('-created_at').first()
    user_code.delete()
    obj,raw_code = ActivationCode.create_for_user(user1)
    gmail(user1,raw_code)
    return redirect('users:verify_code')

@login_required
def signout(request):
    logout(request)
    return redirect('users:signin')    