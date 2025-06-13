from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .forms import SignUpForm,UpdateUserForm


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
    
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
                
            login(request,current_user)
            messages.success(request, "user profile has been updated")
            return redirect('home')
        return render(request, "update_user.html",{'user_form':user_form})
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('home')
            
    return render(request, 'update_user.html')

def home(request):
    products = Product.objects.all()
    categories  = Category.objects.all()
    return render(request,'home.html', {'products':products, 'categories':categories})


def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.method== "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, (" You have been logged in"))
            return redirect('home')
        else:
            messages.error(request, ("Oops! An error occured. Please try again. "))
            return redirect('login')
    else:
        return render(request, 'login.html',{})



    return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have successfully logged out of your account"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request,("Successfully registered."))
            return redirect('home')
        else:
            messages.error(request,("Oops! an error occurred. Please try again later.") )
            return redirect('register')
    else: 
        return render(request,'register.html',{'form': form})


def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product' : product})

def category(request, catname):
    categories = Category.objects.all()

    try:
        category = Category.objects.get(name__iexact=catname)  
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'categories': categories, 'category': category})

    except Category.DoesNotExist:
        messages.error(request, "That category doesn't exist")
        return redirect('home')
