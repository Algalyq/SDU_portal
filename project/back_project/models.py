from django.db import models

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
# Create your models here.
from django.contrib.auth.models import User

Father = 'Father'
Mother = 'Mother'
STATUS_CHOICES = [
        (Father, _("Father")),
        (Mother, _("Mother")),
    ]

GENDER_MALE = 1
GENDER_FEMALE = 2
GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

BA = 'BA'
BSc = 'Bsc'
MA = 'MA'
MSc = 'MSc'
Phd = 'Phd'
Quali_Choices = [
        (BA, _("BA")),
        (BSc, _("BSc")),
        (MA, _("MA")),
        (MSc, _("MSc")),
        (Phd, _("Phd")),
    ]   




IS = 1
CS = 2
Mcm = 3
MathSc = 4
MathPed= 5
TFL = 6
Bioch = 7
Proff_CHOICES = [
        (IS, _("IS")),
        (CS, _("CS")),
        (Mcm, _("Mcm")),
        (MathSc, _("MathSc")),
        (MathPed, _("MathPed")),
        (TFL, _("TFL")),
        (Bioch, _("Bioch")),
    ]   



CSS = 'CSS'
MDE = 'MDE'
INF = 'INF'
PED = 'PED'
ECO= 'ECO'
LAW = 'LAW'
MAT = 'MAT'
COURSE_CHOICES = [
        (CSS, _("CSS")),
        (MDE, _("MDE")),
        (INF, _("INF")),
        (PED, _("PED")),
        (ECO, _("ECO")),
        (LAW, _("LAW")),
        (MAT, _("MAT")),
    ]   

    
AA = 'A+'
A = 'A'
BB = 'B+'
B = 'B'
CC= 'C+'
C = 'C'
D = 'D'
F = 'F'
IP = 'IP'
Em = ' '
MARK_CHOICES = [
        (AA, _("A+")),
        (A, _("A")),
        (BB, _("B+")),
        (B, _("B")),
        (CC, _("C+")),
        (C, _("C")),
        (D, _("D")),
        (F, _("F")),
        (IP, _("IP")),
        (Em, _(" "))
    ]  



class Club(models.Model):
    club_id = models.IntegerField(primary_key=True)
    head = models.CharField(max_length=40)
    club_name = models.CharField(max_length=45,null=True)
    image_club = models.ImageField(upload_to="img/")
    def __str__(self):
        return '%s' % (self.club_id)

class Event(models.Model):
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    event_id = models.IntegerField(primary_key=True)
    event_name = models.CharField(max_length=45)
    starting_date = models.DateField()
    starting_time = models.TimeField()
    ending_date = models.DateField()
    ending_time = models.TimeField()
    activites = models.CharField(max_length=45,null=True)

    def __str__(self):
        return '%s : %s' % (self.event_id, self.activites)

class Teacher(models.Model):
    teacher_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45,null=True)
    last_name = models.CharField(max_length=45,null=True)
    email = models.CharField(max_length=45,null=True)
    password = models.CharField(max_length=45,null=True)
    image_teach = models.ImageField(upload_to='img/',null=True)
    phone = models.CharField(max_length=40,null=True)
    age = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    qualification = models.CharField(choices=Quali_Choices, null=True, blank=True, max_length=25)
    year_of_expr = models.IntegerField(null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return '%s : %s - %s' % (self.teacher_id, self.first_name, self.last_name)



class Adviser_group(models.Model):
    group_id = models.IntegerField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.group_id, self.teacher_id)

class Course_name(models.Model):
    course_code = models.IntegerField(primary_key=True )
    course_name = models.CharField(max_length=45, null=True)

    def __str__(self):
        return '%s' % (self.course_code)


class Teachers_has_course(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_code = models.ForeignKey(Course_name, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=45,null=True)
    last_name = models.CharField(max_length=45,null=True)
    email = models.CharField(max_length=45,null=True)
    password = models.CharField(max_length=45,null=True)
    image_stud = models.ImageField(upload_to='img/')
    phone = models.CharField(max_length=40,null=True)
    current_course = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE, null=True, db_column='club_id', blank=True)
    group_id = models.ForeignKey(Adviser_group, on_delete=models.CASCADE, null=True, db_column='group_id')
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return  '%s' % (self.first_name)
   

   
class Student_has_parent(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    parent_id = models.IntegerField(primary_key=True)

class Parent(models.Model):
    parent_id = models.ForeignKey(Student_has_parent, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=45, null=True)
    last_name = models.CharField(max_length=45, null=True)
    phone = models.CharField(max_length=45, null=True)
    proff = models.CharField(max_length=45,null=True)
    age = models.IntegerField(null=True)
    student_id = models.IntegerField(null=True)
    gender =models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=25)
  

    
class Parent_status(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.parent_id, self.status)

class Faculty(models.Model):
    faculty_id = models.IntegerField(primary_key=True)
    faculty_name = models.CharField(max_length=60, null=True)

    def __str__(self):
        return '%s : %s' % (self.faculty_id, self.faculty_name) 


class Proff(models.Model):
    proff_id =  models.PositiveSmallIntegerField(choices=Proff_CHOICES, null=True, blank=True)
    proff_name = models.CharField(max_length=45, null=True)
    faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.proff_id) 

class Semester(models.Model):
    semester_id = models.IntegerField(primary_key=True)
    current_course = models.IntegerField(null=True)
    season_semester = models.CharField(max_length=40, null=True)

    def __str__(self):
        return '%s' % (self.semester_id)



class Exam(models.Model):
    exam_id = models.IntegerField(primary_key=True)
    exam_name = models.CharField(max_length=45, null=True)

    def __str__(self):
        return '%s : %s' % (self.exam_id, self.exam_name)


class Course(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)  
    course_code = models.CharField(max_length=25, choices=COURSE_CHOICES, null=True)
    course_id = models.IntegerField(null=True)
    course_name = models.CharField(max_length=45, null=True)  
    proff_id = models.ForeignKey(Proff, on_delete=models.CASCADE) 
    semester_id = models.ForeignKey(Semester, on_delete=models.CASCADE)
    grade_id = models.IntegerField(null=True)
    img_course = models.ImageField(upload_to='img/')
    
    def __str__(self):
        return '%s' % (self.id)  

class Grade(models.Model):
    id = models.IntegerField(primary_key=True)
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    grade = models.IntegerField(null=True)
    credit = models.IntegerField(null=True)
    mark = models.CharField(max_length=25, choices=MARK_CHOICES, null=True)
    gpa = models.FloatField(null=True)
    def __str__(self):
        return '%s' % (self.grade)

        
class Attendance(models.Model):
    course_code = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    time_att = models.TimeField(null=True)
    date_att = models.DateField(null=True)
    mark_att = models.BooleanField(null=True)

    def __str__(self):
        return '%s' % (self.course_code)

         
