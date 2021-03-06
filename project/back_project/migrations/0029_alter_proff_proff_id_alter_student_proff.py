# Generated by Django 4.0.2 on 2022-05-23 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0028_student_proff_alter_proff_proff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proff',
            name='proff_id',
            field=models.PositiveSmallIntegerField(blank=True, choices=[('Information Systems', 'Information Systems'), ('Computer Science', 'Computer Science'), ('Math computer model', 'Math computer model'), ('Math Science', 'Math Science'), ('MathPed', 'Math Ped'), ('TFL', 'TFL'), ('Bioch', 'Bioch')], null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='proff',
            field=models.CharField(choices=[('Information Systems', 'Information Systems'), ('Computer Science', 'Computer Science'), ('Math computer model', 'Math computer model'), ('Math Science', 'Math Science'), ('MathPed', 'Math Ped'), ('TFL', 'TFL'), ('Bioch', 'Bioch')], max_length=50, null=True),
        ),
    ]
