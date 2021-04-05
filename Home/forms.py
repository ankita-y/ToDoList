from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Task

class ToDoForm(forms.ModelForm):
    title= forms.CharField(required=False, widget= forms.TextInput(attrs={'placeholder':'Title'}),)
    desc= forms.CharField(required=False, widget= forms.Textarea(attrs={'placeholder':'Enter description here'}),)

    class Meta:
        model = Task
        #fields = ['title','desc','created']
        fields = "__all__"

class Sign_Up(UserCreationForm):
    password2 = forms.CharField(label = 'Confirm Password', widget = forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email Id'} 
    