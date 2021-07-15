from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
# Create your views here.
from .decorators import unauthenticated_user
from .models import Expressions

@unauthenticated_user
def login(request):
    if request.method=='POST':
        nickname = request.POST['nickname']
        password = request.POST['password']
        user=auth.authenticate(username=nickname,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.info(request,"invalid credentials")
            return redirect('login')
    else:
        return render(request,'login.html')
@login_required(login_url="login")
def home(request):
    current_user = request.user
    exp=Expressions.objects.all()
    context={'exp':exp,'id':current_user.id}
    if request.method=='POST':
        expression = request.POST['expression']
        if expression is not None:
            print("hereeeee")
            print(expression)
            result=eval(expression)
            print(result)
            expressions=Expressions()
            expressions.expression=expression
            expressions.result=result
            expressions.save()
            context={'exp':exp,'result':expressions,'id':current_user.id}
        else:
            messages.info(request,"Please fill value")
            return redirect('home')
    print("okk",str(current_user.id))

    return render(request,'index.html',context)

def register(request):
    symbols =['$', '@', '#', '%']
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        nickname=request.POST['nickname']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if len(password1) < 8:
            messages.info(request,'length should be at least 6')            
        if len(password1) > 20:
            messages.info(request,'length should be not be greater than 8')
        if not any(char.isdigit() for char in password1):
            messages.info(request,'Password should have at least one numeral') 
        if not any(char.isupper() for char in password1):
            messages.info(request,'Password should have at least one uppercase letter')            
        if not any(char.islower() for char in password1):
            messages.info(request,'Password should have at least one lowercase letter')            
        if not any(char in symbols for char in password1):
            messages.info(request,'Password should have at least one of the symbols $@#')
        if password1==password2:
            if User.objects.filter(username=nickname).exists():
                messages.info(request,'nickname Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email Taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=nickname,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('login')

        else:
            messages.info(request,"password not matching")
            return redirect('register')
        return redirect('/')

    else:
        return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
def update(request,pk):
    print('in')
    if request.method=='POST':
        symbols =['$', '@', '#', '%']
        user = User.objects.get(id = pk)
        user.first_name = request.POST.get('fname')
        user.last_name = request.POST.get('lname')
        user.password = request.POST.get('password')
      
        if len(user.password) < 8:
            messages.info(request,'length should be at least 6')            
        if len(user.password) > 20:
            messages.info(request,'length should be not be greater than 8')
        if not any(char.isdigit() for char in user.password):
            messages.info(request,'Password should have at least one numeral') 
        if not any(char.isupper() for char in user.password):
            messages.info(request,'Password should have at least one uppercase letter')            
        if not any(char.islower() for char in user.password):
            messages.info(request,'Password should have at least one lowercase letter')            
        if not any(char in symbols for char in user.password):
            messages.info(request,'Password should have at least one of the symbols $@#')
        else:
            user.save()
            messages.success(request, str(user.first_name)+"  profile Update Successfully")
            current_user = request.user
        exp=Expressions.objects.all()
        context={'exp':exp,'id':pk}
        return render(request,'index.html',context)
