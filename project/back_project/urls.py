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
    path('teacher', views.teacher_info, name='teacher'),
    path('term', views.term, name='terms'),
    # Pages for Admin 

    path('admin_page', views.adminka, name='admin_page'),
    path('info_student', views.info_stud, name='student_info'),
    path('search_student', views.search_student, name='searching'),
    path('order_student', views.order_student, name='order'),
    path('info_parent', views.info_parent, name='parent_info'),
    path('search_parent', views.search_parent, name='searching_parent'),
    path('order_parent', views.order_parent, name='order_parent'),
    path('parent_student',views.student_parent, name='parents_info'),
    path('add_user', views.add_user, name='user_add'),
    path('add_student', views.add_student, name='add_student'),
    # Procedure called from Oracle database 
    path('test/<int:id>', views.prod, name='test'),
    
    # adding ali
    path('homePage', views.homePage, name = 'homePage'),


    path('clubs', views.clubs_info, name='clubs'),
    path('club/<int:id>', views.event_info, name='events'),
]

