from django.shortcuts import render, redirect
from django.utils import timezone
from listapp import models
from listapp import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def home(request):
    list_items = models.lists.objects.all().order_by('-added_date', '-time')
    context = {
        'list_items': list_items,
        'user': request.session['id']
    }
    return render(request, "index.html", context)

@login_required(login_url='/login')
def add_lists(request):
    current_date = timezone.now()
    content = request.POST['content']
    models.lists.objects.create(added_date=current_date, text=content)
    return redirect('/')

@login_required(login_url='/login')
def delete(request, id):
    print(id)
    models.lists.objects.get(id=id).delete()
    return redirect('/')

@login_required(login_url='/login')
def profile(request):
    row = User.objects.get(id=request.session['id'])
    context = {
        'row': row,
        'id': request.session['id'],
    }
    return render(request, 'profile.html', context)

def signup(request):
    form = forms.UserForm()
    msg = ""
    if request.method == "POST":
        if request.POST['password'] == request.POST['c_password']:
            row = forms.UserForm(request.POST)
            if row.is_valid():
                s = row.save()
                s.set_password(s.password)
                s.save()
                return redirect('/')
            else:
                msg = "Data not saved"
        else:
            msg = 'Password not matched'
    context = {
        'form': form,
        'msg': msg,
    }
    return render(request, 'signup.html', context)

def log_in(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        atn = authenticate(username=username, password=password)
        if username == '' or password == '':
            msg = 'Please put your username and password'
        elif atn:
            login(request, atn)
            row = User.objects.get(username=username)
            request.session['id'] = row.id
            request.session['user'] = row.is_superuser

            return redirect('/')
        else:
            msg = "Wrong username or password"
    context = {
        'msg': msg,
        'user': 0
    }
    return render(request, 'log_in.html', context)

@login_required(login_url='/login')
def log_out(request):
    logout(request)
    return redirect('/login')
