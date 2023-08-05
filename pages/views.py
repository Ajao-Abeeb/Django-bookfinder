from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.contrib import auth
import requests 
import json


# Create your views here.

@login_required(login_url="login")
def index(request): 
    if request.method == "POST":
         
        text=request.POST['text']
        print(text)
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()   
        result_list = []
        for i in range(10):
            result_dict = {
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('authors'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail') if 'imageLinks' in answer['items'][i]['volumeInfo'] else "",
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            paginator = Paginator(result_list, 6)
            page = request.GET.get('page')
            paged_agent = paginator.get_page(page)
            context={
                'results' :result_list,
                'agent':paged_agent,
            }
        return render(request,'pages/index.html',context)
     
    return render(request, 'pages/index.html')

def signup(request):
    if request.method == 'POST':
         username = request.POST['username']
         email = request.POST['email']
         check = request.POST['check']
         password = request.POST['password']
         con = request.POST['con']
         if password == con:
             if User.objects.filter(email = email).exists():
                 messages.error(request, 'Username already exists')
                 return redirect('signup')
             else:
                user= User.objects.create_user(username=username,email=email,password=password)
                auth.login(request , user)
                messages.success(request, 'You are now logged in')
                return redirect('index')
                user.save()
                messages.success(request, 'You register successfully')
                return redirect('login')
             
         else:
             messages.error(request, 'Password does not match')
             return redirect('signup')
    else:
      return render(request,'pages/signup.html')

def login(request):
    if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']
         user = auth.authenticate(username=username,password=password)
         if user != None :
             auth.login(request , user)
             return redirect('index')
         else:
             messages.error(request ,'Invalid login credentials')
             return redirect('login')
    return render(request , 'pages/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')
        
    return redirect('index')
def about(request):
    return render(request , 'pages/about.html')
 