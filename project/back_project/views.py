from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView,DeleteView,UpdateView
from .forms import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  render, redirect
from django.contrib import messages 
import requests
import os
from .models import *
from django.db import connection
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout 

from django.views.decorators.csrf import csrf_exempt,csrf_protect, requires_csrf_token
from django.db.models import Q



def signin(request):
    if request.user.is_superuser:
        return redirect('admin_page')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                return redirect('admin_page')
            else: 
                return redirect('student',username)
        else:
            form = AuthenticationForm()
            return render(request,'back_project/login.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'back_project/login.html', {'form':form})


def logout_user(request):

    print("there", request)
    logout(request)
    print("here",request)
    return redirect('login')


def homePage(request):

    return render(request, 'back_project/index.html')








def student(request, id):
    student = Student.objects.get(student_id=id)
    course = Course.objects.filter(student_id=id)
    parent_array = []
    total_parent = {}
    student_has_parent = Parent.objects.filter(student_id=id)
    
    
    context = {'student': student, 
                'course': course,
                
                'student_has_parent': student_has_parent
                }
    return render(request, 'back_project/index.html',context )


def term(request):
    course1 = Course.objects.filter(student_id=request.user.username).values('semester_id').distinct().order_by('semester_id')[0:4]
    course2 = Course.objects.filter(student_id=request.user.username).values('semester_id').distinct().order_by('semester_id')[4:8]
    print(course1)
    context = {'course1': course1,'course2': course2}
    return render(request,'back_project/term.html',context)


def course_open(request, id):
    courses = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')
    grade = Grade.objects.filter(student_id=request.user.username).order_by('course_code')

    gpa = Grade.objects.filter(student_id=request.user.username)

    calculate = []
    sum_credit = []

    for i in gpa:
        if i.gpa and i.credit:
            n = i.gpa * i.credit
            calculate.append(n)
            sum_credit.append(i.credit)
        
    sum_gpa = 0
    sum_cre = 0
    for i in calculate:
        sum_gpa += i

    for i in sum_credit:
        sum_cre += i
    total_gpa =  round((sum_gpa ) / sum_cre, 1) 
    print(total_gpa)
    context = {
                'courses': courses,
                'grades': grade,
                'gpa': total_gpa
               }

    return render(request, 'back_project/course.html', context) 



 
def attendance_view(request,id):
    course1 = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[0:3]
    course2 = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[3:6] 
    course3 = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[6:9]
    semester = Semester.objects.all()
    id_course = []
    total_att = {}
    present_att = {}
    absent_att =  {}
    percent_ab = {}
    permit_att = {}
    student_obj = Student.objects.get(student_id=request.user.username)

    for i in course1:
        id_course.append(i.id)

    for i in course2:
        id_course.append(i.id)

    for i in course3:
        id_course.append(i.id)
        
    for i in id_course:

        total_attendance = Attendance.objects.filter(student_id=request.user.username, course_code=i).count()
        total_att[i] =total_attendance
        attendance_present = Attendance.objects.filter(student_id=request.user.username,course_code=i, mark_att=1).count()
        present_att[i]=attendance_present
        attendance_absent =  Attendance.objects.filter(student_id=request.user.username,course_code=i,
                                                       mark_att=0).count()
        absent_att[i]=attendance_absent
        attendance_permit =  Attendance.objects.filter(student_id=request.user.username,course_code=i,
                                                       mark_att=None).count()
        permit_att[i] = attendance_permit


   
        if attendance_absent == 0:
            percent_ab[i] = 0
        else:
            percent_ab[i] = round((attendance_absent / total_attendance) * 100)
    
   
    context = {
        'courses1':course1,
        'courses2':course2,
        'courses3':course3,
        'totals': total_att,    
        'present_att': present_att,
        'absent_att': absent_att,
        'percent_att': percent_ab,
        'permitted_att': permit_att,
        'semester': semester

    }
    return render(request, 'back_project/attendance.html',context )


def attendance_date(request, id):
    course = Course.objects.get(id=id)
    attendance = Attendance.objects.filter(course_code=id).order_by('date_att')
    attendance_present = Attendance.objects.filter(student_id=request.user.username,course_code=id, mark_att=1).count()
    attendance_absent =  Attendance.objects.filter(student_id=request.user.username,course_code=id,mark_att=0).count()
    attendance_perm =  Attendance.objects.filter(student_id=request.user.username,course_code=id,mark_att=None).count()
              
    context = {'courses':course, 'attendance': attendance,
               'attendance_present': attendance_present,
               'attendance_absent': attendance_absent,
               'attendance_permit': attendance_perm}
    return render(request, 'back_project/attendance_date.html', context)


def transcript(request,id):
    
    courses = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[0:3]
    courses1 = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[3:6]
    courses2 = Course.objects.filter(student_id=request.user.username, semester_id=id ).order_by('semester_id')[6:9] 
    grade = Grade.objects.filter(student_id=request.user.username).order_by('course_code')
    semester = Semester.objects.all()
    
    context = {
                'courses': courses,'semester': semester,
                'courses1': courses1,'courses2': courses2,
                'grades': grade,
                'num': id
               }
   
    return render(request, 'back_project/grade_front.html', context )
   
#     query = """
# ;
        
#     """;
#     cursor = connection.cursor()
#     cursor.execute('test_proced1', [request.user.username])
#     result = cursor.fetchall()
    


def grade_test(request,id):
    print(id)
    courses = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[0:3]
    courses1 = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[3:6]
    courses2 = Course.objects.filter(student_id=request.user.username, semester_id=id).order_by('semester_id')[6:9] 
    grade = Grade.objects.filter(student_id=request.user.username).order_by('course_code')
    
    
    context = {
                'courses': courses,
                'courses1': courses1,'courses2': courses2,
                'grades': grade,
                'num': id
               }
    
    return render(request, 'back_project/grade_front.html', context)


def teacher_info(request):
    searched = request.GET.get('searched')
        
    if request.method == "POST":
        searched = request.POST['searched']
        name = Teacher.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched))[0:2]
        name2 = Teacher.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched))[2:4]
        if name | name2:
            return render(request,
                'back_project/teachers_info.html',
                {'searched':searched,
                  'names':name,
                  'names2': name2})
        else:
            name = Teacher.objects.all()[0:3]
            name2 = Teacher.objects.all()[3:6]
            name3 = Teacher.objects.all()[6:9]
            context = {'teacher1': name, 'teacher2': name2, 'teacher3': name3}
            return render(request,'back_project/teachers_info.html', context)
                
    else:
        name = Teacher.objects.all()[0:3]
        name2 = Teacher.objects.all()[3:6]
        name3 = Teacher.objects.all()[6:9]
        context = {'teacher1': name, 'teacher2': name2, 'teacher3': name3}
        return render(request,
                'back_project/teachers_info.html', context)
        

def teacher_students(request):
    searched = request.GET.get('searched')
        
    if request.method == "POST":
        searched = request.POST['searched']
        name = Teacher.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched))[0:2]
        name2 = Teacher.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched))[2:4]
        if name | name2:
            return render(request,
                'back_project/teachers_info.html',
                {'searched':searched,
                  'names':name,
                  'names2': name2})
        else:
            name = Teacher.objects.all()[0:3]
            name2 = Teacher.objects.all()[3:6]
            name3 = Teacher.objects.all()[6:9]
            context = {'teacher1': name, 'teacher2': name2, 'teacher3': name3}
            return render(request,'back_project/teachers_info.html', context)
                
    else:
        name = Teacher.objects.all()[0:3]
        name2 = Teacher.objects.all()[3:6]
        name3 = Teacher.objects.all()[6:9]
        context = {'teacher1': name, 'teacher2': name2, 'teacher3': name3}
        return render(request,
                'back_project/teachers_info.html', context)
        




def adminka(request):
    course = Course.objects.values('course_name').distinct()
    student = Student.objects.all()
    course_name = Course_name.objects.raw('Select distinct count(*) from course')
    teacher = Teacher.objects.all()
    parent = Parent.objects.all()
    events = Event.objects.all()
    club = Club.objects.all()
    context = {
        'courses': course, 'students': student, 'course_names':course_name,
        'teachers': teacher, 'parents': parent,'events': events,
        'clubs':club
    }
    return render(request, 'super_user/user.html',context)


def info_stud(request):

    student = Student.objects.all()
    
    searched = request.GET.get('student_id_sort')

    context = {'student': student}

    return render(request, 'super_user/test.html', context)



def info_parent(request):

    parent = Parent.objects.all()

 
    context = {'parents': parent}

    return render(request, 'super_user/parent_info.html', context)


def delete_parent(request, id):
    parent = Parent.objects.get(parent_id = id).delete()
    return redirect('parent_info')






def clubs_info(request):
    clubs = Club.objects.all()
  
    context = {'clubs':clubs}
    
    return render(request, 'super_user/club.html', context)

def event_info(request, id):
    club = Club.objects.get(club_id=id)
    print(club)
    event = Event.objects.filter(club_id=id)
    context = {'events': event, 'club': club}
    return render(request, 'super_user/events.html',context )


def add_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student')
    else:
        form = UserRegisterForm()
    return render(request, 'super_user/addUser.html', {'form': form,})
    

def add_parent(request):
    if request.method == "POST":
        form = ParentForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('admin_page')
    else:
        form = ParentForm()
    
    return render(request, 'super_user/add_parent.html', {'form': form})
def add_student(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = ProfileForm()
    return render(request, 'super_user/add_student.html' , {'form': form})


def add_club(request):
    if request.method == "POST":
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('clubs')
    else:
        form = ClubForm()
        
    return render(request, 'super_user/add_club.html', {'form': form})

def editParent(request, id):
    parent = Parent.objects.get(parent_id=id)
    if request.method == "POST":
        
        parent.first_name = request.POST.get('first_name')
        parent.last_name = request.POST.get('last_name')
        parent.age = request.POST.get('age')
        parent.phone = request.POST.get('phone')
        parent.proff = request.POST.get('proff')
     
        parent.save()

        messages.success(request, "Succ")   
        return redirect('admin_page')

    context ={'parent': parent}
    return render(request,'super_user/edit_parent.html',context)

def editTeacher(request, id):
    teacher = Teacher.objects.get(teacher_id=id)
    if request.method == "POST":
        
        if len(request.FILES) != 0: 
            if len(teacher.image_teach) > 0:
                os.remove(teacher.image_teach.path)
            
            teacher.image_teach = request.FILES['image_teach']
        teacher.teacher_id = request.POST.get('teacher_id')
        teacher.email = request.POST.get('email')

        teacher.phone = request.POST.get('phone')
        teacher.date_of_birth = request.POST.get('date_of_birth')
        teacher.qualification = request.POST.get('qualification')
        teacher.year_of_expr = request.POST.get('year_of_expr')
        teacher.gender = request.POST.get('gender')
        
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.age = request.POST.get('age')
        teacher.phone = request.POST.get('phone')
       
     
        teacher.save()

        messages.success(request, "Succ")   
        return redirect('admin_page')

    context ={'teacher': teacher}
    return render(request,'super_user/edit_teacher.html',context)


def editStudent(request, id):
    student = Student.objects.get(student_id=id)
    if request.method == "POST":
        if len(request.FILES) != 0: 
            if len(student.image_stud) > 0:
                os.remove(student.image_stud.path)
            
            student.image_stud = request.FILES['image']
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.age = request.POST.get('age')
        student.save()

        messages.success(request, "Succ")   
        return redirect('admin_page')

    context ={'student': student}
    return render(request,'super_user/editStudent.html',context)



def delete_student(request, id):
    student = Student.objects.get(student_id=id).delete()

    return redirect('student_info')
def delete_teacher(request, id):
    teacher = Teacher.objects.get(teacher_id=id).delete()
    
    return redirect('teachers')

def teacher_info(request):

    teacher = Teacher.objects.all()

    context = {'teacher': teacher}

    return render(request, 'super_user/teacher_info.html', context)

def search_teacher(request):

    searched = request.GET.get('searched')

    if request.method == "POST":
        searched = request.POST['searched']
        name = Teacher.objects.filter(Q(first_name__contains=searched) | Q(last_name__contains=searched))
        if name: 
            context = {'searched':searched, 'names': name}
            return render(request, 'super_user/teacher_info.html', context)

    return render(request, 'super_user/teacher_info.html')



def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = TeacherForm()
    return render(request, 'super_user/add_teacher.html' , {'form': form})



def testtable(request):
    return render(request, 'super_user/test.html') 