from django.urls import path

from django.contrib.auth import views as auth_views
from . views import *
from django.contrib.auth import views as auth_views

from .  import views
urlpatterns = [
  
    #LogIn and Logout

    path('', views.signin, name = 'login'),
    path('logout', views.logout_user, name='logout'),

    # Student page for Student

    path('student/<str:id>', views.student, name='student'),
    
    path('course/<int:id>', views.course_open, name='course'),
    path('attendance/<int:id>', views.attendance_view, name='attendance'),
    path('date_att/<int:id>', views.attendance_date, name='date_att'),
    path('transcript/<int:id>', views.transcript, name='transcript'),
    path('/testTr/<int:id>', views.grade_test, name='testTr'),
    path('teacher', views.teacher_students, name='teacher'),
    path('term', views.term, name='terms'),



    # Pages for Admin 

    path('admin_page', views.adminka, name='admin_page'),
    
    
    path('info_student', views.info_stud, name='student_info'),
    
    
    
    path('info_parent', views.info_parent, name='parent_info'),
    path('delete_parent/<int:id>', views.delete_parent, name='parent_delete'),
    
    
    path('add_user', views.add_user, name='user_add'),
    path('add_student', views.add_student, name='add_student'),
    path('edit_student/<int:id>', views.editStudent, name='edit_student'),
    path('delete_student/<int:id>', views.delete_student, name='delete_student'),
    path('add_teacher', views.add_teacher, name='add_teacher'),
    path('teacher_info', views.teacher_info, name='teachers'),
    path('teacher_searching', views.search_teacher, name='searching_teacher'),
    path('add_parent', views.add_parent, name='parent'),
    # Procedure called from Oracle database 
    path('test', views.testtable, name='test'),
    path('edit_parent/<int:id>', views.editParent,name='edit_parent'),
    path('edit_teacher/<int:id>', views.editTeacher, name='edit_teacher'),
    path('delete_teacher/<int:id>', views.delete_teacher, name='delete_teacher'),
    # adding ali
    path('homePage', views.homePage, name = 'homePage'),


    path('clubs', views.clubs_info, name='clubs'),
    path('add_club', views.add_club, name='add_club'),
    
    path('club/<int:id>', views.event_info, name='events'),
]

