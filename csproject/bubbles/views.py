from django.shortcuts import render, redirect
from django.template import loader
from datetime import datetime
from .models import Bubble, User
from .forms import RegistrationForm, LoginForm, ChangePwForm, PostForm

def index(request):
    context = {
        'bubbles' : Bubble.objects.all().order_by('-pub_time'), 
        'user' : request.session['user'] if 'user' in request.session else 'guest', 
        'login_form': LoginForm(),
        'post_form': PostForm()
        }
    return render(request, 'bubbles/index.html', context)

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            request.session['user'] = username
            return redirect('index')
        context = {
            'bubbles' : Bubble.objects.all().order_by('-pub_time'),
            'user': 'guest',
            'login_form': form,
            'post_form' : PostForm()
            }
        return render(request, 'bubbles/index.html', context)
    return redirect('index')

def logout(request):
    request.session['user'] = 'guest'
    return redirect('index')

def register(request):  
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST.get("username")
            request.session['user'] = username
            return redirect('index')
        return render(request, 'bubbles/register.html', {'form': form})        
    form = RegistrationForm()
    return render(request, 'bubbles/register.html', {'form': form})


def userpage(request, username):
    try:
        user = User.objects.get(username=username)
        # user = User.objects.get(username=request.session['user']
        context = {
            'user_bubbles' :  user.bubbles.all().order_by('-pub_time'), 
            'user' : user,
            'post_form' : PostForm(),
            'change_pw_form' : ChangePwForm(),
            }
        return render(request, 'bubbles/userpage.html', context)
    except:
        return redirect('index')

def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            bubble = form.save(commit=False)
            bubble.author = User.objects.get(username=request.session['user'])
            bubble.pub_time = datetime.now()
            bubble.save()
            user = bubble.author
            # user = request.session['user']
            return redirect('userpage', user)
        return redirect('index')
    
def delete_bubble(request, bubble_id):
    bubble = Bubble.objects.get(id=bubble_id)
    user = bubble.author
    # user = request.session['user']
    bubble.delete()
    return redirect('userpage', user)
        

def changepw(request):
    if request.method == 'POST':
        form = ChangePwForm(request.POST)
        user = User.objects.get(username=request.session['user'])
        if form.is_valid():
            user_to_update = form.save(commit=False)
            user_to_update.save()
            return redirect('userpage', request.session['user'])
        context = {
            'user_bubbles' :  user.bubbles.all().order_by('-pub_time'), 
            'user' : user.username,
            'post_form' : PostForm(),
            'change_pw_form' : form,
            }
        return render(request, 'bubbles/userpage.html', context)

    