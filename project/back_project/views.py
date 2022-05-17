from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView,DeleteView,UpdateView
from .forms import *
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import  render, redirect
from django.contrib import messages 
import requests
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
    student_has_parent = Student_has_parent.objects.filter(student_id=id)
    for i in student_has_parent:
        parent_array.append(i.parent_id)
    
    print(parent_array)
    parent_1 = Parent.objects.get(parent_id=parent_array[0])
    print(parent_1)
    parent_2 = Parent.objects.get(parent_id=parent_array[1])

    proff = []
    for i in course:
        proff.append(i.proff_id)
     
    proff = Proff.objects.get(proff_id=str(proff[0]))
    context = {'student': student, 
                'course': course,
                'proff_name': proff,
                'parent_1': parent_1,
                'parent_2': parent_2
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
    # out_val = connection.cursor().var(int)
    # tema = connection.cursor().callfunc('test_gpa',[10, out_val])
    # print(tema)
#     cursor = connection.cursor()
#     cursor.execute('test_proced1', [request.user.username])
#     result = cursor.fetchall()
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
        'permitted_att': permit_att
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
    
    
    context = {
                'courses': courses,
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
            return render(request,
                'back_project/teachers_info.html', context)
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

    return render(request, 'super_user/stud_info.html', context)


def search_student(request):
        searched = request.GET.get('searched')
        
        if request.method == "POST":
            searched = request.POST['searched']
            name = Student.objects.filter(first_name__contains=searched)
           
            return render(request,
                'super_user/stud_info.html',
                {'searched':searched,
                  'names':name})
        elif request.method == "POST":
            searched = request.POST['searched']
            name = Student.objects.filter(first_name__contains!=searched)     
        
            return render(request,'super_user/stud_info.html')



def order_student(request):
        order = request.GET.get('order')
        
        if request.method == "POST":
            order = request.POST['order_sort']
            name = Student.objects.order_by('student_id')
           
            return render(request,
                'super_user/stud_info.html',
                {'order':order,
                  'names':name})
        elif request.method == "POST":
            order= request.POST['order_sort']
            name = Student.objects.order_by('last_name')     
        
            return render(request,'super_user/stud_info.html')


def info_parent(request):

    parent = Parent.objects.all()

 
    context = {'parents': parent}

    return render(request, 'super_user/parent_info.html', context)


def search_parent(request):
        searched = request.GET.get('searched')
        
        if request.method == "POST":
            searched = request.POST['searched']
            name = Parent.objects.filter(first_name__contains=searched)
           
            return render(request,
                'super_user/parent_info.html',
                {'searched':searched,
                  'names':name})
        elif request.method == "POST":
            searched = request.POST['searched']
            name = Parent.objects.filter(first_name__contains!=searched)     
        
            return render(request,'super_user/parent_info.html')



def order_parent(request):
        order = request.GET.get('order')
        
        if request.method == "POST":
            order = request.POST['order_sort']
            name = Parent.objects.order_by('first_name')
           
            return render(request,
                'super_user/parent_info.html',
                {'order':order,
                  'names':name})
        elif request.method == "POST":
            order= request.POST['order_sort']
            name = Parent.objects.order_by('last_name')     
        
            return render(request,'super_user/parent_info.html')


def student_parent(request):
    parents = Parent.objects.filter(student_id=request.user.username)
    num = []
    for i in parents:
        num.append(i.parent_id)
       
    status_parent1 = Parent_status.objects.get(parent_id=num[0])
    status_parent2 = Parent_status.objects.get(parent_id=num[1])
    context = {'parents': parents,
                'status_parent1': status_parent1,
                'status_parent2': status_parent2,
                   }

    

    return render(request, 'back_project/student_parent.html', context)





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
    

def add_student(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_page')
    else:
        form = ProfileForm()
    return render(request, 'super_user/add_student.html' , {'form': form})


def prod(request, id):
    with connection.cursor() as cursor:
        tema = cursor.callproc('delete_stud',[id])
 
    return redirect('admin_page')
