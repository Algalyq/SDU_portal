# Generated by Django 4.0.1 on 2022-05-12 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back_project', '0002_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=45, null=True)),
                ('last_name', models.CharField(max_length=45, null=True)),
                ('email', models.CharField(max_length=45, null=True)),
                ('password', models.CharField(max_length=45, null=True)),
                ('image_teach', models.ImageField(null=True, upload_to='img/')),
                ('phone', models.CharField(max_length=40, null=True)),
                ('age', models.IntegerField(null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('qualification', models.CharField(blank=True, choices=[('BA', 'BA'), ('Bsc', 'BSc'), ('MA', 'MA'), ('MSc', 'MSc'), ('Phd', 'Phd')], max_length=25, null=True)),
                ('year_of_expr', models.IntegerField(null=True)),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], null=True)),
            ],
        ),
    ]