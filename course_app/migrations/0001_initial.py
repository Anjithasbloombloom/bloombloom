# Generated by Django 5.0.2 on 2024-04-01 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(default=None, max_length=20)),
                ('author_img', models.ImageField(default=None, upload_to='authors_img')),
            ],
        ),
        migrations.CreateModel(
            name='Collaborators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collab_name', models.CharField(default=None, max_length=20)),
                ('collab_img', models.ImageField(default=None, upload_to='collab_img')),
            ],
        ),
        migrations.CreateModel(
            name='Educators',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('educator_name', models.CharField(default=None, max_length=20)),
                ('educator_img', models.ImageField(default=None, upload_to='educators_img')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Producers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producer_name', models.CharField(default=None, max_length=20)),
                ('producer_img', models.ImageField(default=None, upload_to='producers_img')),
            ],
        ),
        migrations.CreateModel(
            name='Sectors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_name', models.CharField(default=None, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=20)),
                ('sponsor_img', models.ImageField(default=None, upload_to='sponsors_img')),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_name', models.CharField(default=None, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(default=None, max_length=20)),
                ('topic_desc', models.TextField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_description', models.TextField()),
                ('course_date', models.DateField()),
                ('course_price', models.IntegerField()),
                ('course_learning_credits', models.IntegerField()),
                ('course_lifetime_learners', models.IntegerField(default=None)),
                ('course_rating', models.FloatField()),
                ('course_num_ratings', models.IntegerField()),
                ('course_first_published', models.DateField()),
                ('course_times_launched', models.IntegerField()),
                ('course_num_interested', models.IntegerField()),
                ('course_num_hours', models.IntegerField()),
                ('course_num_days', models.IntegerField()),
                ('course_skills', models.CharField(default=None, max_length=200)),
                ('more_about_course', models.TextField(default=None)),
                ('course_relevance_of_program', models.TextField(default=None)),
                ('course_recommended_learners', models.TextField(default=None)),
                ('course_what_will_learn', models.TextField(default=None)),
                ('course_img', models.ImageField(default=None, upload_to='course_pics')),
                ('course_authors', models.ManyToManyField(default=None, related_name='courses', to='course_app.authors')),
                ('course_collab', models.ManyToManyField(default=None, related_name='courses', to='course_app.collaborators')),
                ('course_medium_of_communication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_app.language')),
                ('course_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course_app.location')),
                ('course_mode', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course_app.mode')),
                ('course_producers', models.ManyToManyField(default=None, related_name='courses', to='course_app.producers')),
                ('course_sponsors', models.ManyToManyField(default=None, related_name='courses', to='course_app.sponsors')),
                ('course_topic', models.ManyToManyField(default=None, related_name='courses', to='course_app.topics')),
            ],
        ),
    ]