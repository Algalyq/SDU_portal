# Generated by Django 4.0.1 on 2022-05-12 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0007_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_has_parent',
            fields=[
                ('parent_id', models.IntegerField(primary_key=True, serialize=False)),
                ('student_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='back_project.student')),
            ],
        ),
    ]
