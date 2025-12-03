from django.shortcuts import render, redirect
from django.template import loader
from .models import Bubble, User

def index(request):
    bubbles = Bubble.objects.all()
    if "user" in request.session:
        user = request.session['user']
    else:
        user = "guest"
    context = {'bubbles' : bubbles, 'user' : user}
    return render(request, 'bubbles/index.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("pw")

        get_user = User.objects.filter(username=username, password=password)
        if get_user:
            request.session['user'] = username
            print(request.session['user'])
        else:
            return redirect('register')
        return redirect('index')

def logout(request):
    request.session['user'] = 'guest'
    return redirect('index')

def register(request):  
    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("pw")
        user = User(username=username,password=password)
        user.save()
        request.session['user'] = username
        return redirect('index')
    else:
        return render(request, 'bubbles/register.html')


def userpage(request, user_username):
    try:
        user = User.objects.get(username=user_username)
        # user = User.objects.get(username=request.session['user'])
        bubbles = user.bubbles.all()
        context = {'user_bubbles' :  bubbles, 'user' : user_username}
        return render(request, 'bubbles/userpage.html', context)
    except:
        return redirect('index')


def post(request):
    return render(request)

