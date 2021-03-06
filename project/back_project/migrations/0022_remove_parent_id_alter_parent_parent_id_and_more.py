# Generated by Django 4.0.1 on 2022-05-18 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0021_alter_course_course_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='id',
        ),
        migrations.AlterField(
            model_name='parent',
            name='parent_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='parent',
            name='student_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='back_project.student'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Student_has_parent',
        ),
    ]
