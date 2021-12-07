from django.urls import path
from .import views

urlpatterns = [
    path ("register/",views.registerPage, name = 'register'),
    path("login/",views.loginPage, name= "login"),
    path("logout/",views.logoutPage, name = "logout"),
    path("",views.home, name= "home"),
    path("student_home/",views.studentHome, name ="student_home"),
    path("add_student/",views.add_student, name ='add_student'),
    path("add_admin/",views.add_admin, name ='add_admin'),
    path("add_subject/",views.add_subject, name ='add_subject'),
    path("get_att/",views.get_att, name ='get_att'),
    path("add_j/", views.add_j, name ='add_j'),
    path("get_subtype/",views.get_subtype, name ='get_subtype'),
    path("full_attendance/",views.full_attendance, name ='full_attendance'),
    path("full_marksheet/",views.full_marksheet, name ='full_marksheet'),
    path("full_skillset/",views.full_skillset, name ='full_skillset'),
    path("result/<regi>", views.search_result, name = 'search_result'),
    path("result1/", views.search_result1, name = 'search_result1'),
    path("result/<result_id>/update", views.update_result, name ='update_result'),
    path("add_result/<regi>/<course_id>", views.add_result, name='add_result'),
    path("search_student_registered/", views.search_student_registered, name = 'search_student_registered'),
    path("get_subtype_networking_marks", views.get_subtype_networking_marks, name = 'get_subtype_networking_marks'),
    path("get_subtype_ai_marks", views.get_subtype_ai_marks, name = 'get_subtype_ai_marks'),
    path("get_subtype_sys_n_media_marks", views.get_subtype_sys_n_media_marks, name = 'get_subtype_sys_n_media_marks'),
    path("get_subtype_dbms_marks", views.get_subtype_dbms_marks, name = 'get_subtype_dbms_marks'),
    path("get_subtype_project_marks", views.get_subtype_project_marks, name = 'get_subtype_project_marks'),
    path("get_subtype_programming_marks", views.get_subtype_programming_marks, name = 'get_subtype_programming_marks'),
    path("get_all_the_marks", views.get_all_the_marks, name = 'get_all_the_marks'),
    path('pdf/', views.GeneratePdf.as_view(),name ="generate_pdf"),
    path('ranksheet/', views.subject_ranksheet,name ="ranksheet"),





]