from django.shortcuts import render, HttpResponse,redirect,HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.
 
#To handle login for the user 
def home_page(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request = request,data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect('/addtask/')
        else:
            form = AuthenticationForm()
        return render(request,'Home.html',{'form':form})
    else:
        return HttpResponseRedirect('/addtask/')

def addtask(request):
    if request.user.is_authenticated:
        # task = Task.objects.all()
        # To get current user specific data
        task = Task.objects.filter(user=request.user)
        
        #create Form object
        form = ToDoForm()
        if request.method == "POST":
            form = ToDoForm(request.POST)
            # To set current user in Django admin
            if form.is_valid():
                fs = form.save(commit=False)
                fs.user = request.user
                fs.save()
            return redirect('/addtask/')      
        
        if request.method == "GET":
            search_input = request.GET.get('search_area') or ''
            if search_input:
                task = Task.objects.filter(user=request.user, title__contains = search_input)

        context ={'task':task,'form':form}
        return render(request,'tasks.html',context)
    else:
        return HttpResponseRedirect('/addtask/')


def handleSignUp(request):
    if request.method == "POST":
        form = Sign_Up(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created successfully')
            return redirect('/')
    else:
        form = Sign_Up()
    return render(request,'signup.html',{'form':form})

def handle_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def updateList(request,pkid):
    task = Task.objects.get(id = pkid)
    form = ToDoForm(instance=task)
    if request.method == "POST":
        form = ToDoForm(request.POST,instance=task)
        if form.is_valid():
            fs = form.save(commit=False)
            fs.user = request.user
            fs.save()
            # form.save()
        return redirect('/addtask/')     
    context = {'form':form}
    return render(request,'update.html',context)

def deleteList(request,pkid):
    task = Task.objects.get(id = pkid)
    form = ToDoForm(instance = task)
    if request.method == "POST":
        task.delete()
        return redirect('/addtask/')
    context = {'task':task}
    return render(request,'delete.html',context)