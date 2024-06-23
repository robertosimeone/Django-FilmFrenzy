from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .forms import SignUpForm
from .models import Movie
from django.shortcuts import get_object_or_404
from .models import Profile
from django.contrib import messages
from .models import User
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Product
from .forms import OrderFormManually
# from .forms import OrderForm
from .models import OrderManually
from .models import Order
from .models import ToDOPage
# Create your views here.

# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created!')
#             return render(request, 'login.html')
#     else:
#         form = SignUpForm()
#     return render(request, 'login.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request,email=email,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,('You have been logged in!'))
            return redirect('homepage')
        else:
            messages.success(request,('There was an error logging in.Please try again...'))
            return redirect('login')

    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,('You have been logged out.'))
    return redirect('homepage')

def home(request):
    user = request.user
    context = {'user':user}
    return render(request,'home.html',context)
def profile(request,pk):
    if request.user.is_authenticated:
        if pk != request.user.id:
            messages.success(request,("You cannot view other peoples profiles"))
            return render(request,'home.html')
        user_id = request.user.id
        profile = Profile.objects.get(user_id = user_id)
        user = request.user 
        context = {
            'profile': profile,
            'user': user
        }

        return render(request, 'profile.html', context)
    else:
        messages.success(request,("You must be logged in to view this page"))
        return render(request,'home.html')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = authenticate(request,email=email,password = password)
            login(request,user)
            messages.success(request,("You have successfully registered!"))
            return redirect('homepage')
    return render(request,'register.html',{'form':form})
def movie_list(request):
    movies = Movie.objects.all()
    return render(request,'movie_list.html',{"movies":movies})
def movie(request,pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST or None)
        movie = Movie.objects.get(id = pk)
        comments = Comment.objects.filter(movie_id = pk).order_by("-created_at")
        user = request.user
        context = {
            'movie':movie,
            'user':user,
            'comments':comments,
            'form':form
        }
        if request.method == 'POST':
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.movie = movie
                comment.save()
                return render(request,"movie.html",context)
            
        if request.method == 'POST':
            action = request.POST['subscribe']
            if action == "unsubscribe":
                user.subscribed_movies.remove(movie)
            elif action == "subscribe":
                if user.token>=movie.price:
                    user.subscribed_movies.add(movie)
                    user.token -=movie.price
                else:
                    messages.success(request,("You don't have enough tokens to subscribe to this movie"))
            user.save()
        return render(request,"movie.html",context)
    else:
        movie = Movie.objects.get(id = pk)
        comments = Comment.objects.filter(movie_id = pk).order_by("-created_at")
        context = {
            'movie':movie,
            'comments':comments,
        }
        return render(request,"movie.html",context)
def update_profile(request,pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id = request.user.id)
        form = UserForm(request.POST or None,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request,'profile.html',{'profile':profile,'user':request.user})
        return render(request,'update_profile.html',{'profile':profile,'user':request.user,'form':form})
    else:
        return redirect('homepage')

def add_funds(request):
    if request.user.is_authenticated:
        products = Product.objects.all()
        context = {
            'products':products,
        }
        return render(request,'add_funds.html',context)
    else:
        return redirect('homepage')
def checkout(request,pk):
    if request.user.is_authenticated:
        product = Product.objects.get(id = pk)
        context={
            'product':product
        }
        return render(request,'checkout.html',context)
    else:
        return redirect('homepage')
def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:',body)
    return JsonResponse('Payment completeed!',safe = False)
def add_funds_manually(request):
    if request.user.is_authenticated:
        user_orders = OrderManually.objects.filter(user_id = request.user.id).order_by('-created_at')
        form = OrderFormManually()
        if request.method == 'POST':
            form = OrderFormManually(request.POST)
            if form.is_valid():
                order = form.save(commit = False)
                order.user = request.user
                order.save()
                user = request.user
                user.token+=order.order_value
                user.save()
                return render(request,'add_funds_manually.html',{'user':request.user,'form':form,'orders':user_orders})
            else:
                 return render(request,'add_funds_manually.html',{"user":request.user,'form':OrderFormManually(),'orders':user_orders})
        else:
            return render(request,'add_funds_manually.html',{"user":request.user,'form':form,'orders':user_orders})
    else:
        return redirect('homepage')

# def todo(request,pk):
#     if request.user.is_authenticated:
#         return render(request,'todo.html',context)
#     else:
#         return redirect('homepage')