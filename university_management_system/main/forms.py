from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Retype Password'

class StudentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = "Student's Name"
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = "Student's Phone"
        self.fields['registration_number'].widget.attrs['class'] = 'form-control'
        self.fields['registration_number'].widget.attrs['placeholder'] = "registration_number"
        self.fields['dept'].widget.attrs['class'] = 'form-control'
        self.fields['dept'].widget.attrs['placeholder'] = 'Department'
        # self.fields['profile_pic'].widget.attrs['class'] = 'file-upload-default'
        # self.fields['profile_pic'].widget.attrs['class'] = 'form-control file-upload-info'
        # self.fields['profile_pic'].widget.attrs['disabled placeholder'] = "Upload Image"

    class Meta:
        model = Student
        fields = ['name','phone','registration_number','dept','profile_pic',]



class AdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = "Admin's Name"
        self.fields['phone'].widget.attrs['class'] = 'form-control'
        self.fields['phone'].widget.attrs['placeholder'] = "Admin's Phone"
        # self.fields['profile_pic'].widget.attrs['class'] = 'file-upload-default'
        # self.fields['profile_pic'].widget.attrs['class'] = 'form-control file-upload-info'
        # self.fields['profile_pic'].widget.attrs['disabled placeholder'] = "Upload Image"
        
    class Meta:
        model = AdminUser
        fields = ['name','phone','profile_pic',]

# class Myform(forms.Form):
#     course_code = forms.CharField(max_length=200)
#     registration_number = forms.CharField(max_length=200)

class UpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs['hidden'] = True
        self.fields['course_code'].widget.attrs['class'] = 'form-control'
        self.fields['course_code'].widget.attrs['readonly'] = True
        self.fields['marks'].widget.attrs['class'] = 'form-control'
        self.fields['attendence'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = Result
        fields = '__all__'


class AddResultForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddResultForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs['hidden'] = True
        self.fields['course_code'].widget.attrs['class'] = 'form-control'
        self.fields['course_code'].widget.attrs['hidden'] = True
        self.fields['marks'].widget.attrs['class'] = 'form-control'
        self.fields['attendence'].widget.attrs['class'] = 'form-control'
    class Meta:
        model = Result
        fields = '__all__'


class AddSubjectForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddSubjectForm, self).__init__(*args, **kwargs)
        self.fields['course_code'].widget.attrs['class'] = 'form-control'
        self.fields['course_code'].widget.attrs['placeholder'] = "Course Code"
        self.fields['subject_name'].widget.attrs['class'] = 'form-control'
        self.fields['subject_name'].widget.attrs['placeholder'] = "Subject's Name"
        self.fields['credit'].widget.attrs['class'] = 'form-control'
        self.fields['credit'].widget.attrs['placeholder'] = "Credit"
        self.fields['subtype'].widget.attrs['class'] = 'form-control'
        self.fields['subtype'].widget.attrs['placeholder'] = "Genre"
    class Meta:
        model = Subject
        fields = '__all__'

