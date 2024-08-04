from django.shortcuts import render,redirect
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms  import SignUpForm
from django import forms

def category(request,foo):
    #replace hyphens with spaces
    foo=foo.replace('-',' ')
    #grab category from url
    try:
        #look up category
        category=Category.objects.get(name=foo)
        products=Product.objects.filter(category=category)
        categories = Category.objects.all()
        return render(request,'category.html',{'products':products,'category':category,'categories': categories})
    
    except:
        messages.success(request,'That category does not exist...')
        return redirect('home')
    
def index(request):
    products=Product.objects.all()
    categories = Category.objects.all()
    return render(request,'index.html',{'products':products,'categories': categories})
def product(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def home(request):
    products=Product.objects.all()
    categories = Category.objects.all()
    
    return render(request,'home.html',{'products':products,'categories': categories})

def about(request):
    return render(request,'about.html',{})

def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Successful')
            return redirect('home')

        
        else:
           messages.success(request,'Please try again there seems to be an error mate')
           return redirect('login')

    else:
         return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,'Logout Successful')

    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Register Successful')
                return redirect('home')
            else:
                messages.error(request, 'Authentication failed. Please try again.')
                return redirect('register')
        else:
            messages.error(request, 'WHOOPS!!! There seems to be an error mate.')
            return render(request, 'login.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'login.html', {'form': form})
    