# university_management_system_extend

This project is the direct extention from the project I did for DBMS Lab..The git link of my dbms project from which I extended it is given Below:
https://github.com/mdneyamul/university_management_system.git (in case , You want to see the commit history)

1. I did this project named "University Management System" because I wanted to Implement DBMS and Software Engineering Pattern that I learned from the theory class properly. 
   Because Something Like University Management Has all the basic CRUD (CREATE, READ, UPDATE, DELETE) Operations, That is essential on learning Database Management System. 
   Also Because of The Supervisor's Advice, I also did many representations with chart.js and other work on the front end which was not the initial plan for this project, 
   I managed to learn some good front end staff with HTML, CSS, and javascript.<br>
   
   <b>Features Of This Project :</b><br><br>
   1.University Management System has 3 groups of users,
           1. <b>Admin</b> 
           2. <b>Teacher</b> 
           3. <b>Student.</b><br>
These 3 group of users have their respective roles and authorizations to perform. And one group can not perform another's task if he doesn't have the authorization.
These kinds of authentications and authorizations are handled by decorators instead of middleware in this project.

<b>****Admin User Functionality:</b> Admin User holds the main administrative role of the application. Only admin has the authorization
to add or remove another admin, teacher, or student user in the 
database. Also, only admin has the roles of Registering a new Course, Department and assigning every course to course teachers.
Then Admin can see an overview of the whole system in the front-end of the admin home page like Teacher's Performance and Department Wise Performance.
<br>
<br>
So in a <b>nutshell</b> Admin's Functionality:<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;1. Add another admin<br>
&nbsp;&nbsp;&nbsp;&nbsp;2. Add a new teacher<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. Add new student<br>
&nbsp;&nbsp;&nbsp;&nbsp;4. Add new department<br>
&nbsp;&nbsp;&nbsp;&nbsp;5. Assign Teachers to  Courses<br>
&nbsp;&nbsp;&nbsp;&nbsp;6. Remove Student<br>
&nbsp;&nbsp;&nbsp;&nbsp;7. Remove Teacher<br>
&nbsp;&nbsp;&nbsp;&nbsp;8. Observe overall feedback ratings of teachers teachings given by students<br>
&nbsp;&nbsp;&nbsp;&nbsp;9. Observe overall performance ranking of Departments<br>
&nbsp;&nbsp;&nbsp;&nbsp;10. Observe overall quantitive factors of university<br>

<br>
<b>***Admin</b><br><br> <br>
<img src="screenshot/01_a.png"/>
<img src="screenshot/2a.png"/>
<img src="screenshot/3a.png"/>
<img src="screenshot/4a.png"/>

<br>
<br>


<b>****Teacher User Functionality:</b> The teacher holds the role of teaching in this web app. First, he is assigned some courses by the admin. 
Then students who want to take the courses, tend to register the courses by sending register requests to the respective teacher who is assigned teacher,
so then the assigned teacher can see the request and can keep it, pending or approve the request or reject it.
If only the request is approved,
then the course is registered for the student and then he can take the course.
otherwise, his result can not be uploaded. Then the teacher can upload his result with JSON file, then he can see his course-wise result.
also can download the "COURSE WISE MARKSHEET" via PDF format.
Teacher can also see various kinds of presentations like perticpation chart course-wise, course wise performance , his session wise courses, and the ratings of teaching
given by the students taking his course.

<br>
So in a <b>nutshell</b> Teacher's Functionality:<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;1. Observe Various representations of Student performance and Student rating feednack and taking courses
&nbsp;&nbsp;&nbsp;&nbsp;2. Approve or Reject register request of Students<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. Add result by JSON file of every course<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. Edit/ Update Result<br>
&nbsp;&nbsp;&nbsp;&nbsp;4. Delete Result<br>
&nbsp;&nbsp;&nbsp;&nbsp;5. See Cousewise result conducted by teacher.<br>
&nbsp;&nbsp;&nbsp;&nbsp;6. Download maksheet as PDF format

<br><br><br>
<b>***Teacher</b><br><br> <br>
<img src="screenshot/01.png"/>
<img src="screenshot/02.png"/>
<img src="screenshot/03.png"/>
<img src="screenshot/04.png"/>
<img src="screenshot/tt.png"/>
<img src="screenshot/05.png"/>
<img src="screenshot/06.png"/>
<img src="screenshot/07.png"/>
<img src="screenshot/08.png"/>
<br>

<br><br><br><b>****Student Functionality:</b> The Student is the main user of the management system. University is managed based on students' needs. So In this web app, a student can see his performance and other things in a very informative way. 
So a student, If he wants to take a course. First, he sends the request to his respective course teacher to register. If the teacher approves the request then only he can sit on the exam and get a result.
Then he can see his result by Genre of that subject. Also, view the skillset him based on the genre.Also he can give ratings of teaching of the teacher on the scale 0 to 5.

<br>
So in a <b>nutshell</b> Student's Functionality:<br><br>
&nbsp;&nbsp;&nbsp;&nbsp;1. Can Send Register Request to course teacher<br>
&nbsp;&nbsp;&nbsp;&nbsp;2. Can see his passing status, registered credit, passed credit etc<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. Can see his skillset by subject genre<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. Can see attendance by barchart<br>
&nbsp;&nbsp;&nbsp;&nbsp;4. Can see his curent markseet<br>
&nbsp;&nbsp;&nbsp;&nbsp;5. Can download marksheet via PDF format.<br>
&nbsp;&nbsp;&nbsp;&nbsp;6. Can see teacher approval table

<b>***Studnet</b><br>
<br>
<br>
<img src="screenshot/01_s.png"/>
<img src="screenshot/02s.png"/>
<img src="screenshot/3s.png"/>
<img src="screenshot/5s.png"/>
<img src="screenshot/6s.png"/>
<img src="screenshot/7s.png"/>
<img src="screenshot/8s.png"/>
<img src="screenshot/9s.png"/>
<img src="screenshot/10s.png"/>
<img src="screenshot/11s.png"/>
<br><br>
<br>
<br>
<br>

2. <b>Installation Procedure:</b> It's A web app with django backend and HTML+CSS+JS front end.<br><br>

&nbsp;&nbsp;&nbsp;&nbsp;1. Install Django==3.1.7<br>
&nbsp;&nbsp;&nbsp;&nbsp;2. Install xhtml2pdf==0.2.5<br>
&nbsp;&nbsp;&nbsp;&nbsp;3. Download the repo then goto the "...\university_management_system_extend\university_management_system>" directory<br>
&nbsp;&nbsp;&nbsp;&nbsp;4. then connect with PostgreSQL type "python manage.py makemigrations" then python manage.py migrate"<br>
&nbsp;&nbsp;&nbsp;&nbsp;5. then create a superuser<br>
&nbsp;&nbsp;&nbsp;&nbsp;6. then type "python manage.py runserver"<br>
&nbsp;&nbsp;&nbsp;&nbsp;7. web app wil be up and running.<br>

<br>






The demo of this project is here: https://youtu.be/2Pi0Oehs6l0

