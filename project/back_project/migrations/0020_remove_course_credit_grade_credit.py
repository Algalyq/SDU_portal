# Generated by Django 4.0.1 on 2022-05-16 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0019_remove_grade_cr_course_credit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='credit',
        ),
        migrations.AddField(
            model_name='grade',
            name='credit',
            field=models.IntegerField(null=True),
        ),
    ]