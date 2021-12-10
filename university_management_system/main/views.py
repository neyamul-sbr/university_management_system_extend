import json
from django.contrib.auth.models import Group
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import *
from django.core import management
from django.core.management.commands import loaddata

#from .EmailBackend import EmailBackend
from .models import *
from .forms import *
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from .decorators import allowed_users, unauthenticated_user,allowed_users_home
from django.http import HttpResponse
from django.views.generic import View

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db import connections
import os
 
def cal_cg(marks):
    if marks>=80:
        return 4.0
    elif marks>=75:
        return 3.75
    elif marks>=70:
        return 3.5
    elif marks>=65:
        return 3.25
    elif marks>=60:
        return 3.00
    elif marks>=55:
        return 2.75
    elif marks>=50:
        return 2.50
    elif marks>=45:
        return 2.25
    elif marks>=40:
        return 2.00
    else:
        return 0.00




##-----------------------------LOG IN AND REGISTER--------------------------------------------------------###

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, "Username Or Password is not Correct")
        

    return render(request, 'login_template/login1.html')

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def registerPageTeacher(request):
    user_form = CreateUserForm(request.POST or None) 
    teacher_form = TeacherForm(request.POST or None, request.FILES or None)
    context = {'teacher_form': teacher_form,'user_form':user_form, 'page_title':'add student'}
    if request.method == 'POST':
        if user_form.is_valid and teacher_form.is_valid():
            user = user_form.save()
            teacher = teacher_form.save()
            teacher.user =user
            teacher.save()
            # username = student_form.cleaned_data.get('username')
            # email = student_form.cleaned_data.get('email')
            # password1 = student_form.cleaned_data.get('password1')
            # password2 = student_form.cleaned_data.get('password2')
            # name = student_form.cleaned_data.get('name')
            # name = student_form.cleaned_data.get('phone')
            # passport = request.FILES['profile_pic']
            # fs = FileSystemStorage()
            # filename = fs.save(passport.name, passport)
            # passport_url = fs.url(filename)
            group = Group.objects.get(name = 'teacher')
            user.groups.add(group)
        else:
            messages.success(request, "Successfully Teacher Added")
    return render(request, 'registration_template/add_teacher.html',context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def registerPage(request):
    user_form = CreateUserForm(request.POST or None) 
    admin_form = AdminForm(request.POST or None, request.FILES or None)
    context = {'admin_form': admin_form,'user_form':user_form, 'page_title':'add student'}
    if request.method == 'POST':
        if user_form.is_valid and admin_form.is_valid():
            user = user_form.save()
            admin = admin_form.save()
            admin.user =user
            admin.save()
            # username = student_form.cleaned_data.get('username')
            # email = student_form.cleaned_data.get('email')
            # password1 = student_form.cleaned_data.get('password1')
            # password2 = student_form.cleaned_data.get('password2')
            # name = student_form.cleaned_data.get('name')
            # name = student_form.cleaned_data.get('phone')
            # passport = request.FILES['profile_pic']
            # fs = FileSystemStorage()
            # filename = fs.save(passport.name, passport)
            # passport_url = fs.url(filename)
            group = Group.objects.get(name = 'admin')
            user.groups.add(group)
        else:
            messages.success(request, "Successfully Admin Added")
    return render(request, 'registration_template/add_admin.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login') 

##-----------------------------------------------LOG IN END -------------------------------------------------------###





##----------------------------------------------- HOME PAGE ----------------------------------------------------------##
@login_required(login_url = 'login')
@allowed_users_home(allowed_roles=['admin', 'teacher'])
def home(request):
    # name = request.user.adminuser.name
    # std1  = Subject.objects.raw('''
    #     SELECT 1 as id, COUNT(*) as cnt
    #     FROM main_student; ''')
    # sub2  =  Subject.objects.raw('''
    #     SELECT 1 as id, COUNT(*) as cnt
    #     FROM main_subject; ''')
    # admin_cnt2 =  Subject.objects.raw('''
    #     SELECT 1 as id, COUNT(*) as cnt
    #     FROM main_adminuser; ''')
    
    # dept_cnt =  Subject.objects.raw('''
    #     SELECT 1 as id, COUNT(*) as cnt
    #     FROM main_student group by dept; ''')
    # cnt1 =0
    # for i in std1:
    #     std = i.cnt
    # for i in sub2:
    #     sub = i.cnt
    # for i in admin_cnt2:
    #     admin_cnt = i.cnt
    # for i in dept_cnt:
    #     cnt1=cnt1+1





    # context = { 'name':name,
    #              'std': std,
    #              'admin_cnt':admin_cnt,
    #              'dept_cnt': dept_cnt,
    #              'sub':sub,
    #              'cnt1':cnt1



    # }
    return render(request,'admin_template/index.html')

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['student'])
def studentHome(request):
    name = request.user.student.name
    regi = request.user.student.registration_number
    dept = request.user.student.dept
    res = Result.objects.filter(student_id = regi).first()
    Subject.objects.raw('''
        SELECT 1 as id, SUM(credit)
        FROM public.main_student JOIN public.main_result ON
        main_student.registration_number = main_result.student_id
        JOIN public.main_subject ON main_result.course_code = main_subject.course_code
        where main_student.registration_number=%s;''',[regi])

    if res == None:
        data = []
        credits = 0
        credits_passed = 0
        percent_passed_credit = 0
        percent_registered = 0
        remain_credit =160
        remain_credit_percent= 100
        current_cgpa =0
        degree_status = "INCOMPLETE"
        remain = "Need to pass "+ str(remain_credit) +" more credits to get a degreee" 
    
    else:
        credits = Subject.objects.raw('''
        SELECT 1 as id, SUM(credit)
        FROM public.main_student JOIN public.main_result ON
        main_student.registration_number = main_result.student_id
        JOIN public.main_subject ON main_result.course_code = main_subject.course_code
        where main_student.registration_number=%s;''',[regi])[0].sum

        credits_passed = Subject.objects.raw('''
        SELECT 1 as id, SUM(credit)
        FROM public.main_student JOIN public.main_result ON
        main_student.registration_number = main_result.student_id
        JOIN public.main_subject ON main_result.course_code = main_subject.course_code
        where main_student.registration_number=%s and marks>=40;''',[regi])[0].sum
        degree_status = ""

 
            

        cgpa = Subject.objects.raw('''
        SELECT 1 as id, credit, marks
        FROM public.main_student JOIN public.main_result ON
        main_student.registration_number = main_result.student_id
        JOIN public.main_subject ON main_result.course_code = main_subject.course_code
        where main_student.registration_number=%s and marks>=40;''',[regi])
        upper =0
        lower = 0
        for k in cgpa:
            upper =upper+ k.credit * cal_cg(k.marks)
            lower =lower + k.credit
        
        current_cgpa = upper/lower
        percent_passed_credit = ((credits_passed)*100)/160


        percent_registered = ((credits)*100)/160

        remain_credit = 160- credits_passed

        remain_credit_percent = ((remain_credit)*100)/160
        remain =""
        if(credits_passed<160):
            degree_status = "INCOMPLETE"
            remain = "Need to pass "+ str(remain_credit) +" more credits to get a degreee" 
        else:
            degree_status = "COMPLETE"
            remain = "Congratulations!!! You are a SUST "+ dept +"Graduate"  

        attendance = Result.objects.raw('''
        SELECT 1 as id, subject_name as sn , attendence as attend FROM
        public.main_student JOIN public.main_result ON
        main_student.registration_number = main_result.student_id
        JOIN public.main_subject ON main_result.course_code = main_subject.course_code
        where main_student.registration_number=%s;''',[regi])
        data = []
        for i in attendance:
            data.append({
                'subject_name': i.sn,
                'attendance'  :i.attend
            })
    context ={'name':name, 
    'credits': credits,
    'percent_registered': percent_registered,
    'credits_passed' : credits_passed,
    'percent_passed_credit': percent_passed_credit,
    'current_cgpa': current_cgpa,
    'degree_status': degree_status,
    'remain': remain,

     
    'data'  : data,
    
    
    }
    return render(request,'student_template/index.html',context)

@login_required(login_url = 'login')
def teacher_home(request):
    return render(request,'teacher_template/index.html')


#--------------------------------------------*****GET*****-------------------------------------------------------------#

@login_required(login_url = 'login')
def get_att(request, *args, **kwargs):
    regi = request.user.student.registration_number
    attendance = Result.objects.raw('''
    SELECT 1 as id, subject_name as sn , attendence as attend FROM
    public.main_student JOIN public.main_result ON
    main_student.registration_number = main_result.student_id
    JOIN public.main_subject ON main_result.course_code = main_subject.course_code
    where main_student.registration_number=%s;''',[regi])
    data =[]
    labels =[]
    for i in attendance:
        labels.append(i.sn)
        data.append(i.attend)

    return JsonResponse(data={
        'labels': labels,
        'data':data,
    })
@login_required(login_url = 'login')
def get_subtype(request, *args, **kwargs):
    regi = request.user.student.registration_number
    subtype = Result.objects.raw('''
    SELECT 1 as id, subtype, SUM(marks) as sum_marks, count(subtype) as cnt FROM
    public.main_student JOIN public.main_result ON
    main_student.registration_number = main_result.student_id
    JOIN public.main_subject ON main_result.course_code = main_subject.course_code
	where registration_number = %s and marks>=40
    group by subtype;''',[regi])

    data =[]
    labels =[]
    for i in subtype:
        labels.append(i.subtype)
        cntt = min(i.cnt*.5,3)
        data.append((i.sum_marks)*7/(i.cnt*100) + cntt)

    return JsonResponse(data={
        'labels': labels,
        'data':data,
    })
def getting_json(subtype, regi):

    marksObj = Result.objects.raw('''
    SELECT 1 as id, subject_name, main_subject.course_code as cc, marks FROM
    public.main_student JOIN public.main_result ON
    main_student.registration_number = main_result.student_id
    JOIN public.main_subject ON main_result.course_code = main_subject.course_code
	where registration_number = %s and subtype = %s;''',[regi,subtype])
    

    subject_name =[]
    course_code =[]
    marks = []
    attr = []
    attr.append("subject_name")
    attr.append("course_code")
    attr.append("marks")
    json_res =[]
    for i in marksObj:
        obj = {}
        obj[attr[0]] = i.subject_name
        print(i.subject_name)
        obj[attr[1]] = i.cc
        obj[attr[2]]= i.marks
        json_res.append(obj) 
    return json_res


def getting_json_result(regi):

    marksObj = Result.objects.raw('''
    SELECT 1 as id, subject_name, main_subject.course_code as cc, marks, attendence as attendance FROM
    public.main_student JOIN public.main_result ON
    main_student.registration_number = main_result.student_id
    JOIN public.main_subject ON main_result.course_code = main_subject.course_code
	where registration_number = %s''',[regi])
    

    subject_name =[]
    course_code =[]
    marks = []
    attr = []
    
    attr.append("subject_name")
    attr.append("course_code")
    attr.append("marks")
    attr.append("attendance")
    attr.append("cgpa")
    json_res =[]
    for i in marksObj:
        obj = {}
        obj[attr[0]] = i.subject_name
        obj[attr[1]] = i.cc
        obj[attr[2]]= i.marks
        obj[attr[3]] = i.attendance
        cgpa = cal_cg(i.marks)
        obj[attr[4]]= cgpa
        json_res.append(obj) 
    return json_res

@login_required(login_url = 'login')
def get_subtype_networking_marks(request, *args, **kwargs):
    regi = request.user.student.registration_number
    subtype = "Networking"
    # subtype = Result.objects.raw('''
    # SELECT 1 as id, subtype, SUM(marks) as sum_marks, count(subtype) as cnt FROM
    # public.main_student JOIN public.main_result ON
    # main_student.registration_number = main_result.student_id
    # JOIN public.main_subject ON main_result.course_code = main_subject.course_code
	# where registration_number = %s and marks>=40
    # group by subtype;''',[regi])

    # marksObj = Result.objects.raw('''
    # SELECT 1 as id, subject_name, main_subject.course_code as cc, marks FROM
    # public.main_student JOIN public.main_result ON
    # main_student.registration_number = main_result.student_id
    # JOIN public.main_subject ON main_result.course_code = main_subject.course_code
	# where registration_number = %s and subtype = 'Networking';''',[regi])
    

    # subject_name =[]
    # course_code =[]
    # marks = []
    # attr = []
    # attr.append("subject_name")
    # attr.append("course_code")
    # attr.append("marks")
    # json_res =[]
    # for i in marksObj:
    #     obj = {}
    #     obj[attr[0]] = i.subject_name
    #     obj[attr[1]] = i.cc
    #     obj[attr[2]]= i.marks
    #     json_res.append(obj) 
    
    json_res = getting_json(subtype, regi)
        

    return JsonResponse(json_res, safe = False)  

@login_required(login_url = 'login')
def get_subtype_dbms_marks(request, *args, **kwargs):
    regi = request.user.student.registration_number
    subtype = "DBMS"
    json_res = getting_json(subtype, regi)
    return JsonResponse(json_res, safe = False) 

@login_required(login_url = 'login')
def get_subtype_ai_marks(request, *args, **kwargs):
    regi = request.user.student.registration_number
    subtype = "AI"
    json_res = getting_json(subtype, regi)
    return JsonResponse(json_res, safe = False)


@login_required(login_url = 'login')
def get_subtype_programming_marks(request, *args, **kwargs):
    regi = request.user.student.registration_number
    subtype = "Programming"
    json_res = getting_json(subtype, regi)
    return JsonResponse(json_res, safe = False)

@login_required(login_url = 'login')
def get_subtype_sys_n_media_marks(request, *args, **kwargs):
    regi = request.user.student.registration_number
    subtype = "System & Multimedia"
    json_res = getting_json(subtype, regi)
    return JsonResponse(json_res, safe = False) 


@login_required(login_url = 'login')
def get_subtype_project_marks(request, *args, **kwargs):
    regi = request.user.student.registration_number
    subtype = "Project"
    json_res = getting_json(subtype, regi)
    return JsonResponse(json_res, safe = False) 


@login_required(login_url = 'login')
def get_all_the_marks(request, *args, **kwargs):
    regi = request.user.student.registration_number
    json_res = getting_json_result(regi)
    return JsonResponse(json_res, safe = False)

def see_registration_status(request, *args, **kwargs):
    regi = str(request.user.student.registration_number)
    print(regi)
    dep = request.user.student.dept
    register = Result.objects.raw('''
    SELECT 1 as id, status, subject_id, dept_id as sub FROM main_registertable
	where student_id = %s ''',[regi])

    for i in register:
        c_id = i.subject_id
        subject_name = Subject.objects.get(course_code = c_id).subject_name       
        i.sub = subject_name
    attr=[]
    attr.append("course_code")
    attr.append("subject_name")
    attr.append("status")
    #attr.append("regi")
    json_res =[]
    for i in register:
        obj = {}
        obj[attr[0]] = i.subject_id
        obj[attr[1]] = i.sub
        obj[attr[2]]= i.status
        #obj[attr[3]]= regi
        json_res.append(obj)
    return JsonResponse(json_res, safe= False)
    
















#------------------------------------------------------***VIEW***-----------------------------------------------------------
@login_required(login_url = 'login')
def full_attendance(request):
    return render(request,'student_template/full_attendance.html')

@login_required(login_url = 'login')
def full_marksheet(request):
    return render(request,'student_template/full_marksheet.html')


@login_required(login_url = 'login')
def full_skillset(request):
    return render(request,'student_template/full_skillset.html')

@login_required(login_url = 'login')
def subject_ranksheet(request):
    regi = request.user.student.registration_number
        
    data = Result.objects.raw('''
    SELECT 1 as id, course_code FROM main_result
	where student_id = %s''',[regi])

    context={'course':data, 'regi': regi} 

    if request.method == 'POST':
        course_id = request.POST.get('course_code')
        marksObj = Result.objects.raw('''
        SELECT 1 as id,main_student.name, main_student.registration_number as regi, marks FROM
        public.main_student JOIN public.main_result ON
        main_student.registration_number = main_result.student_id
        JOIN public.main_subject ON main_result.course_code = main_subject.course_code
	    where main_subject.course_code = %s order by marks DESC;''',[course_id])
        cnt=1
        your_rank = 0
        regi1 = request.user.student.registration_number
        for i in marksObj:
            if i.regi == regi1:
                your_rank = cnt  
            i.id =cnt
            cnt = cnt+1
        subject_name = Subject.objects.get(course_code = course_id).subject_name
        context={'data':marksObj,'course_id':course_id,'subject_name':subject_name, 'rank':your_rank} 
        return render(request, 'student_template/rank_result2.html',context)


    return render(request, 'student_template/rank_result.html',context)

from django.http import HttpResponse
from django.views.generic import View

from main.utils import html_to_pdf 
from django.template.loader import render_to_string
from django.core.files import File
import os
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        regi = request.user.student.registration_number
        name = request.user.student.name
        phone = request.user.student.phone
        email = request.user.email
        dept = request.user.student.dept
        data = Result.objects.raw('''
        SELECT 1 as id, subject_name, main_subject.course_code as cc, marks, attendence as attendance ,student_id as cg , credit FROM
        public.main_student JOIN public.main_result ON
        main_student.registration_number = main_result.student_id
        JOIN public.main_subject ON main_result.course_code = main_subject.course_code
	    where registration_number = %s''',[regi])

        upper =0
        lower = 0
        cgpa = 0
        status =""
        for k in data:
            if k.marks>=40:
                upper =upper+ k.credit * cal_cg(k.marks)
                lower =lower + k.credit
        
        if lower == 0:
            cgpa =0
            
        else:
            cgpa = upper/lower
        if lower<160:
            status = "Incomplete"
        else:
            status = "Complete"

        for i in data:
            i.student_id = cal_cg(i.marks)
                    

        module_dir = os.path.dirname(__file__)  # get current directory
        file_path1 = os.path.join(module_dir, 'templates/student_template/generate_result_pdf_temp.html')
        file_path2 = os.path.join(module_dir, 'templates/student_template/generate_result_pdf.html')

        pwd = os.path.dirname(__file__)
        open(file_path1, "w").write(render_to_string(file_path2, {'data': data,'regi':regi,'name':name, 'phone': phone, 'email':email,'cgpa':cgpa,'status':status,'dept':dept }))

        # Converting the HTML template into a PDF file
        pdf = html_to_pdf(file_path1)
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')






##-----------------------------------------SEARCH------------------------------------####


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def search_result1(request):
    
    if request.method == 'POST':
        registration_number = request.POST.get('registration_number')
        return redirect(reverse('search_result', kwargs={"regi": registration_number}))
       
    return render(request,'admin_template/search_result1.html')

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def search_result(request, regi):
    data = Result.objects.raw('''
        SELECT 1 as id, course_code FROM main_result
	    where student_id = %s''',[regi])

    context={'course':data, 'regi': regi} 
    if request.method == 'POST':
        registration_number = request.POST.get('registration_number')
        course_id = request.POST.get('course_code')
        obj = Result.objects.get(student_id = registration_number ,course_code = course_id)
        id = obj.id
        return redirect(reverse('update_result', kwargs={"result_id": id}))
       
    return render(request,'admin_template/search_result.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def search_student_registered(request):
    
    if request.method == 'POST':
        regi = request.POST.get('registration_number')
        course_id = request.POST.get('course_code')
        res = Student.objects.filter(registration_number = regi).first()
        sub = Subject.objects.filter(course_code = course_id).first()
        if res == None:
            messages.info(request, "The student is not registered..Register the student from here first")
            return redirect(reverse('add_student'))
        if sub == None:
            return HttpResponse("The Subject Is not Registered.. Register The Subject First")
        return redirect(reverse('add_result', kwargs= {"regi": regi, "course_id": course_id}))
    return render(request,'admin_template/search_student_registered.html')
        
###-----------------------------------SEARCH END------------------------------------------------------------------------#

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def update_result(request, result_id):
    result = get_object_or_404(Result, id =result_id)
    form = UpdateForm(request.POST or None, instance = result)
    regi = result.student_id
    context = {'form':form, 'regi': regi}
    if form.is_valid():
        form.save()
    
    return render (request, 'admin_template/update_result.html',context)













#----------------------------------------------** ADD ** -------------------------------------------------------------------------------------------------------


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def add_student(request):
    user_form = CreateUserForm(request.POST or None) 
    student_form = StudentForm(request.POST or None, request.FILES or None)
    context = {'student_form': student_form,'user_form':user_form, 'page_title':'add student'}
    if request.method == 'POST':
        if user_form.is_valid and student_form.is_valid():
            user = user_form.save()
            student = student_form.save()
            student.user =user
            student.save()
            # username = student_form.cleaned_data.get('username')
            # email = student_form.cleaned_data.get('email')
            # password1 = student_form.cleaned_data.get('password1')
            # password2 = student_form.cleaned_data.get('password2')
            # name = student_form.cleaned_data.get('name')
            # name = student_form.cleaned_data.get('phone')
            # passport = request.FILES['profile_pic']
            # fs = FileSystemStorage()
            # filename = fs.save(passport.name, passport)
            # passport_url = fs.url(filename)
            group = Group.objects.get(name = 'student')
            user.groups.add(group)
            messages.success(request, "Successfully Student Added")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'student_template/add_student.html',context)



@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def add_result(request, regi, course_id):
    stu =  get_object_or_404(Student, registration_number = regi)
    res = Result.objects.filter(student_id = regi, course_code = course_id).first()
    if res != None:
        obj = Result.objects.get(student_id = regi ,course_code = course_id)
        id = obj.id
        messages.info(request, "Result Already Exist, You Can Update That Result Here")
        return redirect(reverse('update_result', kwargs= {"result_id": id}))

    form = AddResultForm(request.POST or None, initial ={'student': stu, 'course_code': course_id })
    context = {'form':form, 'regi': regi, 'course_id': course_id}
    if form.is_valid():
        form.save()
    return render(request, 'admin_template/add_result.html',context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def add_subject(request):
    form = AddSubjectForm(request.POST or None)
    context = {'form': form,'page_title':'add subject'}
    if request.method == 'POST':
        if form.is_valid:
            
            c_id = form.cleaned_data.get('course_code') 
            sub = Subject.objects.filter(course_id = c_id).first()
            if sub == None:
                form.save()
                messages.success(request, "Subject Successfully Added")
            else:
                messages.error(request, "Could'nt add subjects.. Subject is Alraeady registered")
        else:
            messages.error(request, "Could'nt add subjects..Probable reasons:<br> 1. Stubject Code and Type not properly entered ")
    return render(request, 'admin_template/add_subject.html',context)



@login_required(login_url = 'login')
@allowed_users(allowed_roles=['teacher'])
def add_j(request):
    data = Result.objects.raw('''
    SELECT 1 as id, course_code FROM main_subject
    ''')

    context={'course':data} 
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        code = request.POST.get('course_code')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        module_dir = 'C:\\Users\\neyamul\\Projects\\university_management_system\\university_management_system\\media'
        file_path =os.path.join(module_dir, filename)

        f =open(file_path)
          
        y=json.load(f)


        for i in range(0, len(y)):
            
            course = code
            regi = y[i]["student_id"]
            marks =y[i]["marks"]
            attendence =y[i]["attendence"]



            cd = Result.objects.filter(student_id = regi, course_code = course).first()
            if cd != None:
                messages.error(request," %s student's  %s course's result already here "% (regi, course))
                continue
            
            sd = Student.objects.filter(registration_number = regi).first()
            if sd == None:
                messages.error(request," %s student is not registered "% (regi))
                continue
            sb = Subject.objects.filter(course_code = course).first()
            if sb == None:
                messages.error(request," %s course is not registered "% (course))
                continue
            # cursor.execute('''INSERT INTO main_result (course_code, marks, attendence, student_id)
            # VALUES (%s,%s,%s,%s );'''% (course, marks, attendence, regi))
            sub = Result(
                student_id = regi,
                course_code =course,
                marks = marks,
                attendence = attendence


            )
            sub.save()
            messages.success(request," %s student's  %s course's result added "% (regi, course))
            
        messages.success(request,"Successfully Added Result for %s course"% (course))  
        return redirect('home') 
            



    return render(request,'admin_template/add_json.html',context)


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def add_admin(request):
    return redirect('register')

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def addDept(request):
    form = DepartmentForm(request.POST or None)
    context = {'form': form, 'page_title':'add department'}
    if request.method == 'POST':
        if form.is_valid:
            form.save()
            messages.success(request,"Successfully Dept. Added")


    return render(request, 'registration_template/add_dept.html',context)
@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin'])
def assign_teacher_dept_search(request):
    data = Result.objects.raw('''
        SELECT dept_id as id FROM main_dept''')

    context={'dept':data} 
    if request.method == 'POST':
        dept_id = request.POST.get('dept_id')
        return redirect(reverse('assign_teacher', kwargs={"dept_id": dept_id}))
       
    return render(request,'admin_template/assign_teacher_dept_search.html',context)

def assign_teacher(request, dept_id):
    data = Result.objects.raw(''' SELECT name as n, teacher_id as id FROM main_teacher where dept_id = %s''', [dept_id])
    student_dept = Result.objects.raw('''SELECT dept_id as id FROM main_dept''')
    course = Result.objects.raw('''SELECT course_code as id, subject_name as name FROM main_subject where dept_id = %s''', [dept_id])
    context = {'teacher':data, 'student_dept':student_dept, 'course': course, 'teacher_dept':dept_id}

    if request.method == "POST":

        stu_dept = request.POST.get('student_dept')
        cour_code = request.POST.get('course')
        t_id   = request.POST.get('teacher')
        t_dept = dept_id


        assingn = AssignedTeacher2(
            student_dept =  stu_dept,
            course_code= cour_code,
            dept_id = t_dept,
            
            teacher_id= t_id,



        )
        assingn.save()
        messages.success(request,"Teacher Id : %s Is Assigned For %s Course In %s Department" %(t_id,cour_code,t_dept))






    return render(request,'admin_template/assign_teacher_dept.html',context)

    




#--------------------------------------------------------###### ADD END #######---------------------------------------------------------



def student_sub_register(request):
    dept_name = request.user.student.dept
    dpt_name =str(dept_name)
    regi = str(request.user.student.registration_number)


    data = AssignedTeacher2.objects.raw('''
        SELECT 1 as id, course_code as cc, teacher_id as tid ,dept_id as did, dept_id as tname FROM main_assignedteacher2
	    where student_dept= %s''', [dpt_name])
    

    for i in data:
        ctt = RegisterTable.objects.filter(subject_id = i.cc, student_id = regi).first()
        
        teacher_name = Teacher.objects.get(teacher_id = i.tid).name
        i.tname = teacher_name
        if ctt != None:
            i.tname = i.tname + "-->Already Requested."
            
    context = {'data':data}

    if request.method == "POST":
        course_cc = request.POST.get('course_regi')
        regi = str(request.user.student.registration_number)

        check = RegisterTable.objects.filter(student_id = regi, subject_id = course_cc).first()
        if check == None:
            print("kk")
            
            ss = RegisterTable(
                 
                dept_id = dpt_name,
                student_id = regi,
                subject_id = course_cc,



            )
            ss.save()
            messages.success(request, "It has gone for approval to Teacher")
            return redirect('home')
        else:
            messages.success(request, "You have already Requested for approval on this Subject. See your Registration table for Registration Status")   
    
    return render(request,'teacher_template/student_sub_register.html',context)


def teacher_approve_search(request):
    teach_id = request.user.teacher.teacher_id
    data = AssignedTeacher2.objects.filter(teacher_id = teach_id)

    context= {'data':data}
    if request.method == "POST":
        course_code_dept = request.POST.get('course_code_dept')
        xx = course_code_dept.split(',')
        return redirect(reverse('teacher_approval', kwargs= {"course_code": xx[0], "student_dept": xx[1]}))






    return render(request, 'teacher_template/teacher_approve_search.html',context)


def teacher_approval(request, course_code, student_dept):
    data2 = Result.objects.raw('''
        SELECT 1 as id, name, student_id, phone, status, profile_pic  FROM
        public.main_student JOIN public.main_registertable ON
        main_student.registration_number = main_registertable.student_id
	    where main_registertable.dept_id = %s and main_registertable.subject_id = %s''',[student_dept,course_code]) 
    data = RegisterTable.objects.filter(subject_id = course_code, dept_id = student_dept)
    stu = []
    for i in data:
        stu.append( Student.objects.filter(registration_number = i.student_id).first())

    
        
    context ={'data':data2,'stu':stu, 'cc': course_code, 'dpt': student_dept}
    if request.method == "POST":
        stat = request.POST.get('optionsRadios')
        xx = stat.split(',')
        print(xx)

        RegisterTable.objects.filter(subject_id = course_code, student_id = xx[1]).update(status = xx[0])




    return render(request, 'teacher_template/teacher_approval.html',context)




    



    


