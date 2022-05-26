from fileinput import FileInput
from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.forms import ImageField, ModelForm, TextInput, Textarea
from django.contrib.auth.models import User


# from Project import author
from .models import Student, Teacher
from django.core.exceptions import ValidationError

from .models import *



class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ['user','student_id','first_name', 'last_name','image_stud','age','date_of_birth', 'proff']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'first_name', 'last_name', 'email', 'image_teach', 
         'phone', 'age', 'date_of_birth', 'qualification', 'year_of_expr', 'gender']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['parent_id', 'first_name','last_name', 'phone', 'proff', 'age','student_id', 'gender', 'status']
 
 
class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['club_id', 'head', 'club_name', 'image_club', 'link_discord', 'link_telegram', 'link_instagram']