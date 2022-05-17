# Generated by Django 4.0.1 on 2022-05-12 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.IntegerField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=45)),
                ('starting_date', models.DateField()),
                ('starting_time', models.TimeField()),
                ('ending_date', models.DateField()),
                ('ending_time', models.TimeField()),
                ('activites', models.CharField(max_length=45, null=True)),
                ('club_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='back_project.club')),
            ],
        ),
    ]
