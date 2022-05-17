# Generated by Django 4.0.1 on 2022-05-12 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0014_exam_format_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(choices=[('CSS', 'CSS'), ('MDE', 'MDE'), ('INF', 'INF'), ('PED', 'PED'), ('ECO', 'ECO'), ('LAW', 'LAW'), ('MAT', 'MAT')], max_length=25, null=True)),
                ('course_id', models.IntegerField(null=True)),
                ('course_name', models.CharField(max_length=45, null=True)),
                ('grade_id', models.IntegerField(null=True)),
                ('img_course', models.ImageField(upload_to='img/')),
                ('proff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_project.proff')),
                ('semester_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_project.semester')),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='back_project.student')),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('grade', models.IntegerField(null=True)),
                ('mark', models.CharField(choices=[('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'), ('C+', 'C+'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('IP', 'IP'), (' ', ' ')], max_length=25, null=True)),
                ('gpa', models.FloatField(null=True)),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_project.course')),
                ('exam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_project.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_project.student')),
            ],
        ),
    ]