# Generated by Django 4.0.2 on 2022-05-23 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0031_alter_teacher_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
