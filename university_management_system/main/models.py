from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Dept(models.Model):
    dept_id = models.CharField(max_length= 3, null=False, primary_key=True)
    name = models.CharField(max_length= 200, null= True)
    def __str__(self):
        return self.dept_id


class Student(models.Model):
    user = models.OneToOneField(User, null = True, on_delete= models.CASCADE)
    registration_number = models.CharField(max_length= 200, null=False, primary_key=True)
    dept = models.ForeignKey(Dept, on_delete= models.CASCADE)
    # is_admin =models.BooleanField(default= True )
    # is_student = models.BooleanField(default= False)
    name = models.CharField(max_length= 200, null= True)
    phone = models.CharField(max_length= 200, null = True)
    profile_pic = models.ImageField(null = True, blank = True)
    
    

    def __str__(self):
        return self.registration_number

class AdminUser(models.Model):
    user = models.OneToOneField(User, null = True, on_delete= models.CASCADE)
    # is_admin =models.BooleanField(default= True )
    # is_student = models.BooleanField(default= False)
    name = models.CharField(max_length= 200, null= True)
    phone = models.CharField(max_length= 200, null = True)
    profile_pic = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, null = True, on_delete= models.CASCADE)
    # is_admin =models.BooleanField(default= True )
    # is_student = models.BooleanField(default= False)
    name = models.CharField(max_length= 200, null= True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length= 200, null=False, primary_key=True)
    phone = models.CharField(max_length= 200, null = True)
    profile_pic = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.name


class AssignedTeacher(models.Model):
    student_dept = models.CharField(max_length= 3)
    dept = models.ForeignKey(Dept,on_delete=models.CASCADE)
    course_code = models.CharField(max_length= 200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("student_dept","course_code"))


class AssignedTeacher2(models.Model):
    student_dept = models.CharField(max_length= 3)
    dept = models.ForeignKey(Dept,on_delete=models.CASCADE)
    course_code = models.CharField(max_length= 200)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("student_dept","course_code"))



class Subject(models.Model):
    course_code = models.CharField(max_length= 200, primary_key= True)
    subject_name = models.CharField(max_length= 200)
    credit = models.FloatField(null = True)
    session = models.CharField(max_length= 200, null = True)
    subtype = models.CharField(max_length= 200, null=True)
    dept =models.ForeignKey(Dept, on_delete=models.CASCADE)

class RegisterTable(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    status = models.CharField(max_length= 200, default= "Pending")
    dept =models.ForeignKey(Dept, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("student","subject"))




class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_code = models.CharField(max_length= 200)
    theory_marks  = models.IntegerField(null = True)
    term_test  = models.IntegerField(null = True)
    attendence = models.IntegerField(null = True)
    total = models.FloatField(null = True)
    dept =models.CharField(max_length= 200)
    class Meta:
        unique_together = (("student","course_code"))
    

class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    rating  = models.IntegerField(default = '3')
    class Metha:
        unique_together = (("student","subject"))









