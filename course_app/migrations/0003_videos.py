# Generated by Django 5.0.3 on 2024-05-07 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_app', '0002_course_temp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=100)),
                ('video', models.FileField(upload_to='video/%y')),
            ],
        ),
    ]